from django.contrib import admin
from .models import Amenity


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "parent",
    )
    list_filter = ("parent",)
    ordering = ("pk",)
    search_fields = ("name",)
