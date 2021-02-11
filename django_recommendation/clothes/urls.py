from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('new-product/', views.ClothCreationView.as_view(), name='new-product'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('like-dislike/', views.product_opinion, name='product-opinion'),
    path('purchase-product/', views.ProductPurchaseView.as_view(), name='purchase-product'),
]
