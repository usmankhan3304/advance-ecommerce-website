from django.contrib import admin
from django.urls import path
from ecomauth import views

urlpatterns = [
    
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.handleout,name="logout"),
    path('activate/<uidb64>/<token>/',views.ActivateAccountView.as_view(),name="activate"),
    path('request-reset-email/',views.ResetEmailPassword.as_view(),name="request-reset-email"),
    path('newpasswrod/<uidb64>/<token>/',views.NewPassword.as_view(),name="newpassword"),
]
