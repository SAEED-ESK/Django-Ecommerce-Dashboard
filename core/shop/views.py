from django.http import JsonResponse
from django.views.generic import (
    View,
    ListView,
    DetailView,
)
from django.core.exceptions import FieldError

from cart.cart import CartSession
from .models import (
    Product,
    ProductCategory,
    WishlistProductModel,
    ProductStatusType
)
from review.models import ReviewModel, ReviewStatusType

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
        context['wishlist_items'] = WishlistProductModel.objects.filter(
            user=self.request.user).values_list('product__id', flat=True) if self.request.user.is_authenticated else []
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
        product = self.get_object()
        context['total_items'] = cart.get_total_items()
        context['is_wished'] = WishlistProductModel.objects.filter(
            user=self.request.user, product__id=product.id).exists() if self.request.user.is_authenticated else False
        context['reviews'] = ReviewModel.objects.filter(product__id=product.id, status=ReviewStatusType.accepted.value)
        return context
    
class AddOrRemoveWishlistView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        message = ''
        if product_id:
            try:
                product_item = WishlistProductModel.objects.get(
                    product__id=product_id, user_id=request.user)
                product_item.delete()
                message = 'محصول با موفقیت از علاقه مندی ها پاک شد.'
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(product_id=product_id, user=request.user)
                message = 'محصول با موفقیت به علاقه مندی ها اضافه شد.'
        return JsonResponse({'message': message})