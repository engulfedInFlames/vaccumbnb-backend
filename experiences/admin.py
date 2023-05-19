from typing import Any
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import Experience
from amenities.models import Amenity
from categories.models import Category


class ExperienceCategoryFilter(SimpleListFilter):
    title = _("category")
    parameter_name = "category"

    def lookups(self, request, model_admin):
        experience_categories = model_admin.model.objects.filter(
            category__kind="experiences"
        )
        category_names = set([ec.name for ec in experience_categories])

        return tuple(
            (category_name, _(category_name)) for category_name in category_names
        )

    def queryset(
        self, request: Any, queryset: QuerySet[Experience]
    ) -> QuerySet[Experience] | None:
        result = queryset.filter(category__name=self.value())
        return result


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "start",
        "end",
        "created_at",
    )
    list_filter = (ExperienceCategoryFilter,)

    def formfield_for_manytomany(
        self,
        db_field,
        request: HttpRequest | None,
        **kwargs: Any,
    ) -> ModelMultipleChoiceField:
        # queryset에 데이터를 할당하지 않으면 전체 데이터를 불러온다.
        if db_field.name == "amenities":
            kwargs["queryset"] = Amenity.objects.filter(parent="experience")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(
        self,
        db_field,
        request: HttpRequest | None,
        **kwargs: Any,
    ) -> ModelChoiceField | None:
        # queryset에 데이터를 할당하지 않으면 전체 데이터를 불러온다.
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(kind="experience")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
