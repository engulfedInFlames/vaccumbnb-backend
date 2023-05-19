from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import House
from users.serializers import TinyUserSerializer
from amenities.serializers import AmenityListSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class CreateHouseSerializer(ModelSerializer):
    class Meta:
        model = House
        exclude = ("host",)


class HouseListSerializer(ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = SerializerMethodField()
    is_host = SerializerMethodField()

    def get_rating(self, house):
        return house.rating()

    def get_is_host(self, house):
        user = self.context.get("user")
        if user:
            return house.host == user

    class Meta:
        model = House
        exclude = (
            "host",
            "category",
        )


class HouseDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    amenities = AmenityListSerializer(many=True)
    photos = PhotoSerializer(many=True)

    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_on_wishlist = SerializerMethodField()
    reviews = SerializerMethodField()

    def get_rating(self, house):
        return house.rating()

    def get_is_host(self, house):
        user = self.context.get("user")
        if user:
            return house.host == user
        return False

    def get_reviews(self, house):
        return house.reviews.all().count()

    def get_is_on_wishlist(self, house):
        user = self.context.get("user")
        if user:
            # 1. 해당 user의 wishlist를 쿼리
            # 2. 해당 wishlist에 id가 일치하는 house를 쿼리
            is_house_on_wishlist = Wishlist.objects.filter(
                user=user,
                houses__pk=house.pk,
            ).exists()
            return is_house_on_wishlist

        return False

    class Meta:
        model = House
        fields = "__all__"
        read_only_fields = (
            "category",
            "photos",
        )
