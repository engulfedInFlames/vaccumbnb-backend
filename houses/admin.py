from django.contrib import admin
from .models import House, Amenity


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "host",
        "created_at",
        "updated_at",
        )

    list_filter = (
        "country",
        "city",
        "pet_allowed",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
        )


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
