from django import forms
from django.utils import timezone

from .models import UserAddressModel, CouponModel

class OrderCheckoutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCheckoutForm, self).__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get('address_id')
        try:
            address = UserAddressModel.objects.get(id=address_id, user=self.request.user)
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("Invalid address for the requested user.")
        return address
    
    def clean_coupon(self):
        code = self.cleaned_data.get('coupon')
        if code == '':
            return None
        
        coupon = None
        try:
            coupon = CouponModel.objects.get(code=code)

        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("کد تخفیف وارد شده وجود ندارد.")
        
        if coupon:
            if coupon.used_by.count() > coupon.max_limit_usage:
                raise forms.ValidationError('محدودیت در تعداد استفاده')
            
            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("کد منقضی شده است.")
            
            if self.request.user in coupon.used_by.all():
                raise forms.ValidationError("از کد تخفیف قبلا استفاده کرده اید.")
        
        return coupon

