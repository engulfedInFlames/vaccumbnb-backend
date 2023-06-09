from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "kind",
    )
    list_filter = ("kind",)
    ordering = ("pk",)
    search_fields = ("name",)
