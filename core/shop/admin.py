from django.contrib import admin
from .models import (
    Product,
    ProductCategory,
    ProductImageModel,
    WishlistProductModel
)

class CustomProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel
    extra = 1
    fields = ("file",)

@admin.register(Product)
class CustomProductAdmin(admin.ModelAdmin):
    models = Product
    list_display = (
        "id",
        "title",
        "stock",
        "status",
        "created_date",
    )

@admin.register(ProductCategory)
class CustomProductCategoryAdmin(admin.ModelAdmin):
    models = ProductCategory
    list_display = (
        "id",
        "title",
        "created_date",
    )

@admin.register(ProductImageModel)
class CustomProductImageModelAdmin(admin.ModelAdmin):
    models = ProductImageModel
    list_display = (
        "id",
        "file",
        "created_date",
    )

@admin.register(WishlistProductModel)
class CustomWishlistProductModelAdmin(admin.ModelAdmin):
    models = WishlistProductModel
    list_display = (
        "id",
        "user",
        "product",
    )
