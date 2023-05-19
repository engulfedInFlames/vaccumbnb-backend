from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>/",
        views.ReviewDetail.as_view(),
        name="review_detail",
    )
]
