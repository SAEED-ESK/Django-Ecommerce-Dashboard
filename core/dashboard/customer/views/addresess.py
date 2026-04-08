from django.views.generic import (
    ListView, UpdateView, DeleteView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import FieldError

from order.models import UserAddressModel
from ...permissions import CustomerHasAccessPermission
from ..forms import CustomerAddressForm

class CustomerAddressListView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/customer/addresses/address-list.html'

    def get_queryset(self):
        queryset = UserAddressModel.objects.filter(user=self.request.user)
        order_by = self.request.GET.get('order_by')
        if order_by:
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
class CustomerAddressCreateView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    CreateView
):
    form_class = CustomerAddressForm
    template_name = 'dashboard/customer/addresses/address-create.html'
    success_message = "آدرس با موفقیت ایجاد شد."
    success_url = reverse_lazy("dashboard:customer:address-list")

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class CustomerAddressEditView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
):
    form_class = CustomerAddressForm
    template_name = 'dashboard/customer/addresses/address-edit.html'
    success_message = "آدرس با موفقیت به روز شد."

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:customer:address-edit",
            kwargs={'pk':self.get_object().pk}
        )
    
class CustomerAddressDeleteView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'dashboard/customer/addresses/address-delete.html'
    success_message = "آدرس با موفقیت حذف شد."
    success_url = reverse_lazy("dashboard:customer:address-list")

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
