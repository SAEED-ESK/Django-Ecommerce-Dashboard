from django.urls import path
from .. import views

urlpatterns = [
    path('product/list/', views.AdminProductListView.as_view(), name='product-list'),
    path('product/create/', views.AdminProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/edit/', views.AdminProductEditView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete/', views.AdminProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>/images/create/',
         views.AdminProductImagesCreateView.as_view(),
         name='product-images-create'
    ),
    path('product/<int:pk>/images/<int:image_id>/delete/',
         views.AdminProductImagesRemoveView.as_view(),
         name='product-images-remove'
    ),
]