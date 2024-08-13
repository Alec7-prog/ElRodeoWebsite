from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("cart", views.cart, name="cart"),
    path("menu", views.menu, name="menu"),
    path("register", views.register, name="register")
]