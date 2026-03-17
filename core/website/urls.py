from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('submit-ticket/', views.SendContactFormView.as_view(), name='submit-ticket'),
    path('subscribe/', views.NewsLetterView.as_view(), name='news-letter'),
]