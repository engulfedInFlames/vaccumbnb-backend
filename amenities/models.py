from django.db import models
from django.conf import settings

from common.models import CommonModel


class Amenity(CommonModel):

    """Amenity Model Definiton

    parent가 house이면 description에 null을 할당한다.
    """

    class ParentGroupChoices(models.TextChoices):
        HOUSE = "house", "House"
        EXPERIENCE = "experience", "Experience"

    name = models.CharField(
        max_length=150,
    )
    detail = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    parent = models.CharField(
        max_length=20,
        choices=ParentGroupChoices.choices,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="amenities",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
