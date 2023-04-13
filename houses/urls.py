from django.urls import path
from . import views

urlpatterns = [
    path("", views.Houses.as_view(), name="all_houses"),
    path("<int:id>/", views.HouseDetail.as_view(), name="only_one_house"),
    path("amenities/", views.Amenities.as_view(), name="all_amenities"),
    path("amenities/<int:id>", views.AmenityDetail.as_view(), name="only_one_amenity"),
]
