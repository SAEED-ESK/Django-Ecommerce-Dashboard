from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.OrderCheckoutView.as_view(), name='checkout'),
    path('completed/', views.OrderCompletedView.as_view(), name='completed'),
    path('failed/', views.OrderFailedView.as_view(), name='failed'),
    path('coupon/check/', views.CouponCheckView.as_view(), name='coupon-check'),
]