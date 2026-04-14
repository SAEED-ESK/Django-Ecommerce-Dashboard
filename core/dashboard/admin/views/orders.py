from django.views.generic import (
    ListView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError

from order.models import OrderModel, OrderStatusType
from ...permissions import AdminHasAccessPermission

class AdminOrderListView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/admin/orders/order-list.html'
    paginate_by = 3

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = OrderModel.objects.all()
        order_by = self.request.GET.get('order_by')
        status = self.request.GET.get('status')
        search_q = self.request.GET.get('q')
        if status:
            queryset = queryset.filter(status=status)
        if search_q:
            queryset = queryset.filter(id__contains=search_q)
        if order_by:
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['status_types'] = OrderStatusType.choices
        return context
    
class AdminOrderDetailView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    DetailView
    ):
    template_name = 'dashboard/admin/orders/order-detail.html'
    queryset = OrderModel.objects.all()