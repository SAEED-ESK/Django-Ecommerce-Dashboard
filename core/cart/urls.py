from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('session/add-product/', views.SessionAddProduct.as_view(), name='session-add-product'),
    path('session/session-update-product-quantity/', views.SessionProductUpdateQuantityView.as_view(), name='session-update-product-quantity'),
    path('session/session-remove-product/', views.SessionProductRemoveView.as_view(), name='session-remove-product'),
    path('summary/', views.CartSummary.as_view(), name='cart-summary'),
]