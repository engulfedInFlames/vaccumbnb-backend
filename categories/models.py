from django.db import models
from common.models import CommonModel


class Category(CommonModel):

    """Category for House or Experience"""

    class Meta:
        verbose_name_plural = "Categories"

    class CategoryKindChoices(models.TextChoices):
        HOUSE = "houses", "Houses"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()} : {self.name}"
