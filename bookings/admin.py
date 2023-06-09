from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "pk",
        "kind",
        "user",
        "house",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "guests",
    )
    list_filter = ("kind",)
