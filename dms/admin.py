from django.contrib import admin
from .models import DMRoom, DM


@admin.register(DMRoom)
class DMRoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
        )
    list_filter = ("created_at",)


@admin.register(DM)
class DMAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "room",
        "created_at",
        )
    list_filter = ("created_at",)