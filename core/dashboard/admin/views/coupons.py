from django.views.generic import (
    ListView, UpdateView, DeleteView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import FieldError

from order.models import CouponModel
from ...permissions import AdminHasAccessPermission
from ..forms import AdminCouponForm

class AdminCouponListView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/admin/coupons/coupon-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = CouponModel.objects.all()
        search_q = self.request.GET.get('q')
        order_by = self.request.GET.get('order_by')
        if search_q:
            queryset = CouponModel.objects.filter(code__icontains=search_q)
        if order_by:
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context

class AdminCouponCreateView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    CreateView
):
    form_class = AdminCouponForm
    template_name = 'dashboard/admin/coupons/coupon-create.html'
    success_message = "کد تخفیف با موفقیت ایجاد شد."
    success_url = reverse_lazy("dashboard:admin:coupon-list")
    
class AdminCouponEditView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
):
    form_class = AdminCouponForm
    queryset = CouponModel.objects.all()
    template_name = 'dashboard/admin/coupons/coupon-edit.html'
    success_message = "کد تخفیف با موفقیت به روز شد."

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:coupon-edit",
            kwargs={'pk':self.get_object().pk}
        )
    
class AdminCouponDeleteView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    DeleteView
):
    queryset = CouponModel.objects.all()
    template_name = 'dashboard/admin/coupons/coupon-delete.html'
    success_message = "کد تخفیف با موفقیت حذف شد."
    success_url = reverse_lazy("dashboard:admin:coupon-list")

