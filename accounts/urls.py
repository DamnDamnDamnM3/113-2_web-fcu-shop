from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.get_cart, name="get_cart"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/", views.remove_cart_item, name="remove_cart_item"),
    path("favorites/", views.get_favorites, name="get_favorites"),
    path("favorites/add/", views.add_to_favorites, name="add_to_favorites"),
    path(
        "favorites/remove/", views.remove_from_favorites, name="remove_from_favorites"
    ),
]
