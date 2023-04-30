from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    """Photo Model Definition"""

    def __str__(self):
        return "Photo File"

    file = models.URLField()
    description = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )


class Video(CommonModel):

    """Video Model Definition"""

    def __str__(self):
        return "Video File"

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
