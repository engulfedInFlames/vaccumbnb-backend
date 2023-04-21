from django.urls import path
from . import views

urlpatterns = [
    path("", views.Houses.as_view(), name="all_houses"),
    path("<int:id>/", views.HouseDetail.as_view(), name="only_one_house"),
    path("<int:id>/reviews", views.HouseReviews.as_view(), name="house_reviews"),
    path("<int:id>/amenities", views.HouseAmenities.as_view(), name="house_amenities"),
    path("amenities/", views.Amenities.as_view(), name="all_amenities"),
    path("amenities/<int:id>", views.AmenityDetail.as_view(), name="only_one_amenity"),
    path("<int:id>/photos", views.HousePhotos.as_view(), name="all_photos"),
    path("<int:id>/bookings", views.HouseBookings.as_view(), name="all_bookings"),
]
