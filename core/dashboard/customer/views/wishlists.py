from django.views.generic import (
    ListView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy

from shop.models import WishlistProductModel
from ...permissions import CustomerHasAccessPermission

class CustomerWishlistListView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/customer/wishlists/wishlist-list.html'
    paginate_by = 3

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = WishlistProductModel.objects.filter(user=self.request.user)
        order_by = self.request.GET.get('wishlist_by')
        search_q = self.request.GET.get('q')
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
        return context
    
class CustomerWishlistDeleteView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    SuccessMessageMixin,
    DeleteView
    ):
    http_method_names = ['post']
    success_url = reverse_lazy('dashboard:customer:wishlist-list')
    success_message = "محصول با موفقیت حذف شد."

    def get_queryset(self):
        return WishlistProductModel.objects.filter(user=self.request.user)