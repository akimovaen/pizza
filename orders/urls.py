from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("shopping_cart", views.shopping_cart, name="shopping_cart"),
    path("delete_dish", views.delete_dish, name="delete_dish"),
    path("place_order", views.place_order, name="place_order"),
]
