from django.urls import path
from . import views

urlpatterns = [
    path("", views.Wishlists.as_view(), name="all_wishlists"),
    path("<int:id>", views.WishlistDetail.as_view(), name="only_one_wishlist"),
    path(
        "<int:id>/houses/<int:house_id>",
        views.WishlistFlipper.as_view(),
        name="wishlist_flipper",
    ),
]
