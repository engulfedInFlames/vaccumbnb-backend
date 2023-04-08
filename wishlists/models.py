from django.db import models
from common.models import CommonModel
from django.conf import settings


class Wishlist(CommonModel):

    """ Wishlist Model Definition """
    
    def __str__(self) -> str:
        return self.name
    
    name = models.CharField(
        max_length=150,
    )
    houses = models.ManyToManyField(
        "houses.House",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

