from django.contrib import admin
from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import *

app_name = "cart" 

urlpatterns = [
    
    path('', login_required(CartView.as_view()), name="cart-list"),
    path('<int:pk>/add-to-cart/', login_required(addToCartView.as_view()),name="cart-add"),
    path('checkout/', login_required(CheckOutView.as_view()),name="checkout")
]
