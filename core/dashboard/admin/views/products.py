from django.views.generic import (
    ListView, UpdateView, DeleteView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import FieldError

from shop.models import Product, ProductStatusType, ProductCategory
from ...permissions import AdminHasAccessPermission
from ..forms import AdminProductEditForm

class AdminProductListView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/admin/products/product-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset =     queryset = Product.objects.all()
        search_q = self.request.GET.get('q')
        category_id = self.request.GET.get('category_id')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        order_by = self.request.GET.get('order_by')
        if search_q:
            queryset = Product.objects.filter(title__icontains=search_q)
        if category_id:
            queryset = Product.objects.filter(category__id=category_id)
        if min_price:
            queryset = Product.objects.filter(price__gte=min_price)
        if max_price:
            queryset = Product.objects.filter(price__lte=max_price)
        if order_by:
            try:
                queryset = Product.objects.order_by(order_by)
            except FieldError:
                pass
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategory.objects.all()
        return context
    
class AdminProductCreateView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    CreateView
):
    form_class = AdminProductEditForm
    template_name = 'dashboard/admin/products/product-create.html'
    success_message = "محصول با موفقیت ایجاد شد."
    success_url = reverse_lazy("dashboard:admin:product-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class AdminProductEditView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
):
    form_class = AdminProductEditForm
    queryset = Product.objects.all()
    template_name = 'dashboard/admin/products/product-edit.html'
    success_message = "محصول با موفقیت به روز شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={'pk':self.get_object().pk})
    
class AdminProductDeleteView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    DeleteView
):
    queryset = Product.objects.all()
    template_name = 'dashboard/admin/products/product-delete.html'
    success_message = "محصول با موفقیت حذف شد."
    success_url = reverse_lazy("dashboard:admin:product-list")