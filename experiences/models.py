from django.db import models
from common.models import CommonModel
from django.conf import settings


class Experience(CommonModel):

    """Experience Model Definiiton"""

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    amenities = models.ManyToManyField(
        "amenities.Amenity",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="experiences",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
