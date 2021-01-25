from django.contrib import admin
from django.urls import path

from django.conf.urls import url 
from django.contrib.auth.decorators import login_required

from .views import *
from cart.views import *
app_name = "products" 

urlpatterns = [
    path('', productList.as_view(), name="products-list"),
    path('<str:slug>/<int:pk>/', productDetails.as_view(),name="products-details"),
    path('add/', login_required(addProductView.as_view()),name="products-form"),
    path('<int:pk>/remove-from-cart/', login_required(removeCartView.as_view()),name="cart-remove"),
    path('oops/', productOops.as_view(),name="oops"),
    path('<int:pk>/whishlist/',login_required(WishList.as_view()), name="wishlist"), 
    path('wishlist/',login_required(WishListView.as_view()),name="wishlist-view"),

]
