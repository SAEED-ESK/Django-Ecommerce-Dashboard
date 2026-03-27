from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from accounts.models import Profile
from ..forms import CustomerChangePasswordForm, CustomerProfileEditForm
from ...permissions import CustomerHasAccessPermission

class CustomerSecurityEditView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    auth_views.PasswordChangeView,
    SuccessMessageMixin,
    TemplateView
    ):
    form_class = CustomerChangePasswordForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    template_name = 'dashboard/customer/profile/security-edit.html'
    success_message = "رمز عبور با موفقیت به روز شد."

class CustomerProfileEditView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
    ):
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    template_name = 'dashboard/customer/profile/profile-edit.html'
    success_message = "پروفایل با موفقیت به روز شد."

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    
class CustomerProfileImageEditView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
    ):
    http_method_names = ['post']
    model = Profile
    fields = ['image']
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "عکس پروفایل با موفقیت به روز شد."

    def get_object(self, queryset = None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'مشکلی در آپلود عکس به وجود آمده است.لطفا مجددا امنتحان کنید.'
            )
        return redirect(self.success_url)
    
    