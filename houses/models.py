from django.db import models
from django.conf import settings
from common.models import CommonModel


class House(CommonModel):

    """House Model Definition"""

    # 첫 번째 인자를 꼭 "self"로 할 필요 X, 인자만 있으면 된다.
    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            # self.reviews.all()을 하게 되면 review의 전체 DB 데이터를 가지고 오게 된다.
            # 필요한 것은 rating 뿐이므로, 필터링 (Optimization)
            for value in self.reviews.all().values("rating"):
                total_rating += value["rating"]
            return round(total_rating / count, 2)

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

    """Amenity Model Definiton"""

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
