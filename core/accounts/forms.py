from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import UserCreationForm

class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError("User email is not verified!")

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('email', 'password', 'password1')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')

        if password != password1:
            raise ValidationError("کلمه عبور و تکرار آن یکسان نیستند.")
        
        if password:
            validate_password(password)

        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user