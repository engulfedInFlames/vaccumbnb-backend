from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, House
from wishlists.models import Wishlist
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer

# from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
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
        # 다른 Field와의 데이터 연동을 확장한다. 필요에 따라 확장할 것. 또한, 사용자 정의할 수 없다는 단점이 있다.
        # depth = 1

    def get_rating(self, house):
        return house.rating()

    def get_is_host(self, house):
        user = self.context.get("user")
        return house.host == user


class HouseDetailSerializer(ModelSerializer):
    # 다른 Field와의 관계를 수동으로 정의해줄 필요가 있다.
    # read_only = True 라서 update가 안 된다.
    host = TinyUserSerializer(read_only=True)

    amenities = AmenitySerializer(
        many=True,
        read_only=True,
    )
    # array이면 many=True
    category = CategorySerializer(
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    # 새로 정의하는 필드는 참조하는 model(여기서는 House)의 field명과 중복돼서는 안 된다.
    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_on_wishlist = SerializerMethodField()
    reviews = SerializerMethodField()

    def get_rating(self, house):
        return house.rating()

    def get_is_host(self, house):
        user = self.context.get("user")
        if user.is_authenticated:
            return house.host == user
        return False

    def get_reviews(self, house):
        return house.reviews.all().count()

    def get_is_on_wishlist(self, house):
        user = self.context.get("user")
        if user.is_authenticated:
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
