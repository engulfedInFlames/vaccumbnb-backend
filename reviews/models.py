from django.db import models
from common.models import CommonModel
from django.conf import settings


class Review(CommonModel):

    """ Review from a User to a House or Experience"""

    def __str__(self) -> str:
        return f"{self.user} | {self.rating} ⭐"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    house = models.ForeignKey(
        "houses.House",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()
