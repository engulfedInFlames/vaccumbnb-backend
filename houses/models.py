from django.db import models
from django.conf import settings
from common.models import CommonModel


class House(CommonModel):

    """ House Model Definition """

    def __str__(self):
        return self.name

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire Place"
        PRIVATE_ROOM = "private_room", "Private Room"
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_allowed = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="houses",
    )
    amenities = models.ManyToManyField(
        "houses.Amenity",
        related_name="houses",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="houses",
    )


class Amenity(CommonModel):

    """ Amenity Model Definiton """

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
