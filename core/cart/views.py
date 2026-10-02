from django.views import View
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse

from .cart import CartSession

class SessionAddProduct(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        cart.add_or_update(
            product_id=product_id, quantity=1, keyword='add'
        )
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {
                'cart': cart.get_cart_dict(), 
                'total_quantity': cart.total_quantity()
            })
    
class SessionProductUpdateQuantityView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart.add_or_update(product_id, quantity, 'update')
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {
                'cart': cart.get_cart_dict(), 
                'total_quantity': cart.total_quantity()
            })
    
class SessionProductRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse(
            {
                'cart': cart.get_cart_dict(), 
                'total_quantity': cart.total_quantity()
            })
       
class CartSummary(TemplateView):
    template_name = 'cart/cart_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context['total_items'] = cart.get_total_items()
        context['total_quantity'] = cart.total_quantity()
        context['total_payment_price'] = cart.get_total_payment_price()
        return context