from django.urls import path

from . import views

urlpatterns = [
    path("", views.AmenityList.as_view()),
    path("<int:id>", views.AmenityDetail.as_view()),
]
