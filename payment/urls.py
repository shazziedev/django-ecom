from django.contrib import admin
from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import *

app_name = "payment" 

urlpatterns = [
    
    path('process/', login_required(payment_process), name="process"),
    path('done/', login_required(payment_done),name="done"),
    path('canceled/', login_required(payment_canceled),name="canceled"),

]
