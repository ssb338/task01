from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    path("create/", views.create_shop, name="create-shop"),
    path("list/", views.shop_list, name="shop-list"),
    path("update/<int:pk>/", views.update_shop, name="update-shop"),
    path("location/", views.location_view, name="location"),
    path(
        "shops_within_distance/",
        views.shop_within_distance,
        name="shops-within-distance",
    ),
]
