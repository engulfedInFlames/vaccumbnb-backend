from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.MyWishlist.as_view(),
        name="my_wishlist",
    ),
    path(
        "<int:pk>/houses/<int:house_pk>",
        views.ToggleHouseOnWishlist.as_view(),
        name="toggle_house_on_wishlist",
    ),
    path(
        "<int:pk>/experiences/<int:experience_pk>",
        views.ToggleExperienceOnWishlist.as_view(),
        name="toggle_experience_on_wishlist",
    ),
]
