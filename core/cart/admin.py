from django.contrib import admin
from .models import CartModel, CartItemModel

@admin.register(CartModel)
class CustomCartModelAdmin(admin.ModelAdmin):
    models = CartModel
    list_display = (
        "id",
        "user",
        "created_date",
    )

@admin.register(CartItemModel)
class CustomCartItemModelAdmin(admin.ModelAdmin):
    models = CartItemModel
    list_display = (
        "id",
        "product",
        "cart",
        "quantity",
        "created_date",
    )

