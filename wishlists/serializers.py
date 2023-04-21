from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from houses.serializers import HouseListSerializer


class WishlistSerializer(ModelSerializer):
    houses = HouseListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "name",
            "houses",
        )
