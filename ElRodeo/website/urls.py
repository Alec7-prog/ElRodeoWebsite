from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="default"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart", views.cart, name="cart"),
    path("menu", views.menu, name="menu"),
    path("register", views.register, name="register")
]