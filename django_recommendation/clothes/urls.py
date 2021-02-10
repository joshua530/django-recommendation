from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('new-product/', views.create_product, name='new-product'),
]
