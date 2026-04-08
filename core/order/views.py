from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse_lazy
from django.utils import timezone

from .permissions import CustomerHasAccessPermission
from .models import CouponModel, UserAddressModel, OrderModel, OrderItemModel
from .forms import OrderCheckoutForm
from cart.models import CartModel
from cart.cart import CartSession
from decimal import Decimal

class OrderCheckoutView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    FormView,
):
    template_name = 'order/checkout.html'
    form_class = OrderCheckoutForm
    success_url = reverse_lazy('order:completed')

    def get_form_kwargs(self):
        kwargs = super(OrderCheckoutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        coupon = cleaned_data['coupon']
        cart = CartModel.objects.get(user=self.request.user)
        order = OrderModel.objects.create(
            user=self.request.user,
            address = address.address,
            state = address.state,
            city = address.city,
            zip_code = address.zip_code,
        )
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price()
            )
        total_price = order.calculate_total_price()
        if coupon:
            total_price = total_price - round(total_price * Decimal(coupon.discount_percent / 100))
            order.coupon = coupon
            coupon.used_by.add(self.request.user)

        order.total_price = total_price
        order.save()
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        cart = CartModel.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context['total_price'] = total_price
        context['total_tax'] = round(total_price*9/100)
        return context
    
class OrderCompletedView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    TemplateView,
):
    template_name = 'order/completed.html'

class CouponCheckView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    View,
):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        
        status_code = 200
        message = 'کد تخفیف با موفقیت اعمال شد.'
        total_price = 0
        total_tax = 0
        try:
            coupon = CouponModel.objects.get(code=code)

        except CouponModel.DoesNotExist:
            status_code, message = 404, "کد تخفیف وارد شده وجود ندارد."
        
        else:
            if coupon.used_by.count() > coupon.max_limit_usage:
                status_code, message = 403, 'محدودیت در تعداد استفاده'
            
            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, "کد منقضی شده است."
            
            elif self.request.user in coupon.used_by.all():
                status_code, message = 403, "از کد تخفیف قبلا استفاده کرده اید."
            
            else:
                cart = CartModel.objects.get(user=self.request.user)
                total_price = cart.calculate_total_price()
                total_price = total_price - round(total_price * Decimal(coupon.discount_percent / 100))
                total_tax = round(total_price*9/100)

        
        return JsonResponse(
            {
                'message':message,
                'total_price': total_price,
                'total_tax':total_tax
            },
                status=status_code
        )