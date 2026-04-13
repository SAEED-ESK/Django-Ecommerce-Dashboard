from django.views.generic import (
    ListView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import FieldError

from order.models import OrderModel, OrderStatusType
from ...permissions import CustomerHasAccessPermission

class CustomerOrderListView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/customer/orders/order-list.html'
    paginate_by = 3

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user)
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
    
class CustomerOrderDetailView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    DetailView
    ):
    template_name = 'dashboard/customer/orders/order-detail.html'

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)