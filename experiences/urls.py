from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.ExperienceList.as_view(),
        name="experience_list",
    ),
    path(
        "<int:pk>/",
        views.ExperienceDetail.as_view(),
        name="experience_detail",
    ),
    path(
        "<int:pk>/reviews/",
        views.ExperienceReviews.as_view(),
        name="experience_bookings",
    ),
    path(
        "<int:pk>/amenities/",
        views.ExperienceAmenities.as_view(),
        name="experience_amenities",
    ),
    path(
        "<int:pk>/bookings/",
        views.ExperienceBookings.as_view(),
        name="experience_bookings",
    ),
    path(
        "<int:pk>/photos/",
        views.ExperiencePhotos.as_view(),
        name="experience_photos",
    ),
]
