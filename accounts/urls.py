from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/", views.remove_cart_item, name="remove_cart_item"),
    path("cart/", views.get_cart, name="get_cart"),
]
