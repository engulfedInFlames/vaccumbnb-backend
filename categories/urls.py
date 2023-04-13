from django.urls import path
from . import views

# Router를 사용하는 것은 독이 될 수 있다.

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="all_categories",
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",  # all()에서 하나를 검색; retrieve는 기본으로 "pk"를 받게 되어 있다. 다른 이름을 사용할시 사용자 설정해야 한다.
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
        name="one_category",
    ),
]
