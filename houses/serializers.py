from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import House
from users.serializers import TinyUserSerializer
from amenities.serializers import AmenityListSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


class CreateHouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = (
            "country",
            "city",
            "name",
            "price",
            "rooms",
            "address",
            "kind",
            "toilets",
            "description",
            "pet_allowed",
            "amenities",
            "category",
        )


class HouseListSerializer(ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    rating = SerializerMethodField()
    is_host = SerializerMethodField()

    class Meta:
        model = House
        fields = (
            "id",
            "rating",
            "country",
            "city",
            "name",
            "description",
            "price",
            "amenities",
            "photos",
            "is_host",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }
        # 다른 Field와의 데이터 연동을 확장한다. 필요에 따라 확장할 것. 또한, 사용자 정의할 수 없다는 단점이 있다.
        # depth = 1

    def get_rating(self, house):
        return house.rating()

    def get_is_host(self, house):
        user = self.context.get("user")
        if user:
            return house.host == user


class HouseDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)

    amenities = AmenityListSerializer(many=True)

    photos = PhotoSerializer(many=True)

    # 새로 정의하는 필드는 참조하는 model(여기서는 House)의 field명과 중복돼서는 안 된다.
    category = SerializerMethodField()
    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_on_wishlist = SerializerMethodField()
    reviews = SerializerMethodField()

    def get_category(self, house):
        return house.category

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
                houses__id=house.id,
            ).exists()
            return is_house_on_wishlist

        return False

    class Meta:
        model = House
        fields = (
            "id",
            "name",
            "rating",
            "is_on_wishlist",
            "host",
            "country",
            "city",
            "address",
            "price",
            "kind",
            "rooms",
            "toilets",
            "description",
            "pet_allowed",
            "category",
            "reviews",
            "amenities",
            "photos",
            "is_host",
        )
        read_only_fields = (
            "category",
            "photos",
        )
