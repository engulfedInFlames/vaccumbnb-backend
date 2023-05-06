from django.urls import path
from . import views

# Router를 사용하는 것은 독이 될 수 있다.

urlpatterns = [
    path(
        "houses/",
        views.HouseCategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "experiences/",
        views.ExperienceCategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "houses/<int:pk>/",
        views.HouseCategoryViewSet.as_view(
            {
                "get": "retrieve",  # all()에서 하나를 검색; retrieve는 기본으로 "pk"를 받게 되어 있다. 다른 이름을 사용할시 사용자 설정해야 한다.
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "experiences/<int:pk>/",
        views.ExperienceCategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
