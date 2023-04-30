from django.urls import path
from . import views


urlpatterns = [
    path("perks/", views.Perks.as_view(), name="all_perks"),
    path("perks/<int:id>/", views.PerkDetail.as_view(), name="only_one_perk"),
]
