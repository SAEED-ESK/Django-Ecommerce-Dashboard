from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .forms import AuthenticationForm
from .utils import send_async_email

import threading

class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass

class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")
    html_email_template_name = 'registration/password_reset_email.html'

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context, from_email,
            to_email,
            html_email_template_name=None
        ):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        
        html_body = ""
        if html_email_template_name:
            html_body = render_to_string(html_email_template_name, context)
            
        send_async_email(subject, html_body, [to_email])

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass