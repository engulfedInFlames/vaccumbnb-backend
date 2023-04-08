from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    """ Photo Model Definition """
    
    def __str__(self):
        return "Photo File"
    
    
    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )



class Video(CommonModel):
    
    """ Video Model Definition """
    
    def __str__(self):
        return "Video File"
    
    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
