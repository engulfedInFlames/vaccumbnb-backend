from django.db import models
from common.models import CommonModel
from django.conf import settings


class DMRoom(CommonModel):

    """ DMRoom Model Definition"""

    def __str__(self):
        return "DM Room"

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="DMRooms",
    )


class DM(CommonModel):

    """ DM Model Definition """

    def __str__(self):
        return f"{self.user} says: {self.text}"

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="DMs"
    )
    room = models.ForeignKey(
        "dms.DMRoom",
        on_delete=models.CASCADE,
        related_name="DMs"
    )
