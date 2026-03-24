from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.core.exceptions import FieldError

from cart.cart import CartSession
from .models import Product, ProductStatusType, ProductCategory

class ProductGridView(ListView):
    template_name = 'shop/product_grid.html'
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset =     queryset = Product.objects.filter(
        status=ProductStatusType.publish.value
        )
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

class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    queryset = Product.objects.filter(
        status=ProductStatusType.publish.value
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context['total_items'] = cart.get_total_items()
        return context