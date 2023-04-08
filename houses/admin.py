from django.contrib import admin
from .models import House, Amenity


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "host",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_allowed",
        "kind",
        "amenities",
    )

    # models에서도, admin에서도 list_display 내에 들어갈 변수를 정의할 수 있다.
    def total_amenities(self, house):
        return house.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
