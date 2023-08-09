from django.contrib import admin
from django.urls import path
from ecomauth import views

urlpatterns = [
    
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.handleout,name="logout"),
]
