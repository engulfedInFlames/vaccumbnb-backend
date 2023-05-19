from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.Houses.as_view(),
        name="house_list",
    ),
    path(
        "<int:pk>/",
        views.HouseDetail.as_view(),
        name="house_detail",
    ),
    path(
        "<int:pk>/reviews/",
        views.HouseReviews.as_view(),
        name="house_reviews",
    ),
    path(
        "<int:pk>/amenities/",
        views.HouseAmenities.as_view(),
        name="house_amenities",
    ),
    path(
        "<int:pk>/bookings/",
        views.HouseBookings.as_view(),
        name="house_bookings",
    ),
    path(
        "<int:pk>/photos/",
        views.HousePhotos.as_view(),
        name="house_photos",
    ),
]
