from django.urls import path
from . import views

# Router를 사용하는 것은 독이 될 수 있다.

urlpatterns = [
    path(
        "<int:pk>/",
        views.CategoryDetail.as_view(),
        name="category_deatil",
    )
]
