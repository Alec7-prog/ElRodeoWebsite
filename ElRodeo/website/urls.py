from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart, name="cart"),
    path("menu/", views.menu, name="menu_view"),
    path("register/", views.register, name="register"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),

    path("update_item/", views.updateItem, name="update_item")
]