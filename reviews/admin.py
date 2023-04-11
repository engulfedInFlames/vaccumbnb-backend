from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Words"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        # super().lookups(request, model_admin)
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        # super().queryset(request, reviews)
        # request.GET으로 parameter의 key와 value를 dict 형태로 가지고 올 수 있다.
        # ↓ shortcut
        param = self.value()
        if param:
            return reviews.filter(payload__contains=param)
        else:
            return
        # ALL Option을 선택하거나, "Clear all filters"를 하면 word에 None이 할당되고, None으로는 filter X
        # Filter를 연속으로 선택하면 filter chaning도 할 수 있다.


class GoodFilter(admin.SimpleListFilter):
    title = "Good or Bad"

    parameter_name = "evaluation"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"), ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        param = self.value()
        if param:
            if param == "good":
                return reviews.filter(rating__gte=3)
            else:
                return reviews.filter(rating__lt=3)
        else:
            return


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = ("rating", "house__name", WordFilter, GoodFilter,)
