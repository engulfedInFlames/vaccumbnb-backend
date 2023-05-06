from django.urls import path
from . import views


urlpatterns = [
    path("", views.ExperienceList.as_view()),
    path("<int:id>", views.ExperienceDetail.as_view()),
]
