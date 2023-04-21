from django.urls import path
from . import views

urlpatterns = [
    path("photos/<int:id>", views.PhotoDetail.as_view(), name="only_one_photo")
]
