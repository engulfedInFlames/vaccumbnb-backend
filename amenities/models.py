from django.db import models
from django.conf import settings


from common.models import CommonModel


class Amenity(CommonModel):

    """
    Amenity Model Definiton
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
        on_delete=models.SET_NULL,
        related_name="amenities",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
