from shop.models import Product, ProductStatusType

class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart",
        {
            "items": [],
            "total_price": 0,
            "total_items": 0
        })

    def product_update_quantity(self, product_id, quantity):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                item['quantity'] = int(quantity)
                break
        else:
            return

        self.save()

    def add_product(self, product_id):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                item['quantity'] += 1
                break

        else:
            new_item = {
                "product_id": product_id,
                "quantity": 1,
            }
            self._cart['items'].append(new_item)
        self.save()

    def get_cart_dict(self):
        return self._cart
    
    def get_total_items(self):
        cart_items = self._cart["items"]
        for item in cart_items:
            product_obj = Product.objects.get(
                id=item['product_id'],
                status=ProductStatusType.publish.value
            )
            item['product_obj'] = product_obj
            item['total_price'] = int(item['quantity']) * product_obj.get_price()

        return cart_items
    
    def total_quantity(self):
        all_quantity = 0
        for item in self._cart['items']:
            all_quantity += item['quantity']

        return all_quantity
    
    def get_total_payment_price(self):
        total_payment_price = 0
        for item in self._cart['items']:
            total_payment_price += item['total_price']

        return total_payment_price
    
    def remove_product(self, product_id):
        for item in self._cart['items']:
            if product_id == item['product_id']:
                self._cart['items'].remove(item)
                break
        else:
            return

        self.save()

    def clear(self):
        self._cart = self.session['cart'] = {
            "items": [],
            "total_price": 0,
            "total_items": 0
        }

    def save(self):
        self.session.modified = True