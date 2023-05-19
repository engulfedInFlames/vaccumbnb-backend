from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>",
        views.AmenityDetail.as_view(),
        name="amenity_detail",
    ),
]
