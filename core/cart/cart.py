from typing import List, Dict, Any
from django.contrib.sessions.backends.base import SessionBase
from shop.models import Product, ProductStatusType
from .models import CartModel, CartItemModel

class CartSession:
    def __init__(self, session: SessionBase):
        self.session: SessionBase = session
        self._cart: Dict[str, Any] = self.session.setdefault(
            "cart",
            {
                "items": [],
                "total_price": 0,
                "total_items": 0
            }
        )

    def _get_product_objects(self) -> Dict[int, Product]:
        """تمام محصولات موجود در سبد را با یک کوئری دریافت می‌کند."""
        product_ids = [item['product_id'] for item in self._cart['items']]
        products = Product.objects.filter(
            id__in=product_ids,
            status=ProductStatusType.publish.value
        )
        return {product.id: product for product in products}

    def _find_item(self, product_id: int):
        """
        یک متد کمکی برای پیدا کردن ایندکس و آیتم محصول در لیست.
        """
        for index, item in enumerate(self._cart['items']):
            if item['product_id'] == product_id:
                return index, item
        return None, None

    def add_or_update(self, product_id: int, quantity: int, keyword: str) -> None:
        """
        افزودن محصول به سبد یا به‌روزرسانی تعداد آن.
        اگر محصول وجود نداشته باشد، ایجاد می‌شود.
        اگر وجود داشته باشد، تعداد آن به مقدار جدید تغییر می‌کند.
        """
        quantity = int(quantity)
        if quantity < 1:
            return

        index, item = self._find_item(product_id)

        if item is not None:
            if keyword == 'add':
                # محصول وجود دارد: تعداد را آپدیت کن
                self._cart['items'][index]['quantity'] += quantity
            elif keyword == 'update':
                self._cart['items'][index]['quantity'] = quantity
        else:
            # محصول وجود ندارد: آیتم جدید بساز
            new_item = {
                "product_id": product_id,
                "quantity": quantity,
            }
            self._cart['items'].append(new_item)
        
        self.save()

    def remove_product(self, product_id: int) -> None:
        """
        حذف محصول از سبد خرید.
        """
        original_length = len(self._cart['items'])
        self._cart['items'] = [item for item in self._cart['items'] if item['product_id'] != product_id]
        
        if len(self._cart['items']) != original_length:
            self.save()

    def get_cart_dict(self) -> Dict[str, Any]:
        return self._cart

    def get_total_items(self) -> List[Dict[str, Any]]:
        products_map = self._get_product_objects()
        valid_items = []

        for item in self._cart['items']:
            product = products_map.get(int(item['product_id']))
            if product:
                item['product_obj'] = product
                item['total_price'] = int(item['quantity']) * product.get_price()
                valid_items.append(item)
        
        return valid_items

    def total_quantity(self) -> int:
        return sum(item['quantity'] for item in self._cart['items'])

    def get_total_payment_price(self) -> int:
        total_price = 0
        products_map = self._get_product_objects()
        
        for item in self._cart['items']:
            product = products_map.get(int(item['product_id']))
            if product:
                total_price += int(item['quantity']) * product.get_price()
                
        return total_price

    def clear(self) -> None:
        self._cart = self.session['cart'] = {
            "items": [],
            "total_price": 0,
            "total_items": 0
        }

    def save(self) -> None:
        self.session.modified = True

    def sync_cart_items_from_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        for cart_item in cart_items:
            for item in self._cart['items']:
                if str(cart_item.product.id) == item['product_id']:
                    cart_item.quantity = item['quantity']
                    cart_item.save()
                    break
            else:
                new_item = {
                "product_id": str(cart_item.product_id),
                "quantity": cart_item.quantity,
                }
                self._cart['items'].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()

    def merge_session_cart_in_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        for item in self._cart['items']:
            product_obj = Product.objects.get(
                id=item['product_id'],
                status=ProductStatusType.publish.value
            )
            cart_item, created = CartItemModel.objects.get_or_create(cart=cart, product=product_obj)
            cart_item.quantity = item["quantity"]
            cart_item.save()
        
        session_product_ids = [item['product_id'] for item in self._cart['items']]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()
