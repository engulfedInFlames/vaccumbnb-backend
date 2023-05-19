from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>",
        views.BookingDetail.as_view(),
        name="booking_detail",
    ),
]
