from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile

class AdminChangePasswordForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control text-center'
        self.fields['old_password'].widget.attrs['placeholder'] = 'پسورد قدیمی خود را وارد کنید.'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control text-center'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'پسورد جدید خود را وارد کنید.'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control text-center'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'پسورد جدید خود را مجدد وارد کنید.'

    error_messages = {
        "password_incorrect": _(
            "پسورد قدیمی وارد شده اشتباه است.لطفا دوباره تلاش کنید."
        ),
        "password_mismatch": _("دو پسورد وارد شده باهم تطابق ندارند!"),
    }

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control text-center'