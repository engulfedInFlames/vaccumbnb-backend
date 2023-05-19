from rest_framework.serializers import ModelSerializer

from .models import Wishlist
from houses.serializers import HouseListSerializer
from experiences.serializers import ExperienceListSerializer


class WishlistSerializer(ModelSerializer):
    houses = HouseListSerializer(
        many=True,
        read_only=True,
    )
    experiences = ExperienceListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "houses",
            "experiences",
        )
