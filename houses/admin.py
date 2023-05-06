from django.contrib import admin
from django.db.models.query import QuerySet
from .models import House


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, houses):
    # model_admin: 해당 decorator가 추가될 ModelAmdin 객체
    # request: request에 대한 정보. 특히, user 정보
    # queryset: 체크박스로 선택된 데이터들의 모음. 여기서는 houses
    if request.user.is_superuser:
        for house in houses.all():
            house.price = 0
            house.save()


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "host",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_allowed",
        "kind",
    )

    # 기본적으로 django는 __contains로 검색
    search_fields = (
        "name",
        "host__username",
        # "^name", # ← __startswith
        # "=name", # ← equal
    )

    actions = (reset_prices,)

    # models에서도, admin에서도 list_display 내에 들어갈 변수를 정의할 수 있다.
    # def total_amenities(self, house):
    #     return house.amenities.count()
