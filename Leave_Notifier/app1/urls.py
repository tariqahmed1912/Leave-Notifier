from django.contrib import admin
from django.urls import path, include
from app1 import views

urlpatterns = [
    path('', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('home', views.home, name="home"),
    path('check', views.check, name="check")
    #path('form',views.form, name="form"),
]