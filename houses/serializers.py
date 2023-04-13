from rest_framework.serializers import ModelSerializer
from .models import Amenity, House
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class HouseListSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"
        # 다른 Field와의 데이터 연동을 확장한다. 필요에 따라 확장할 것. 또한, 사용자 정의할 수 없다는 단점이 있다.
        # depth = 1


class HouseDetailSerializer(ModelSerializer):
    # 다른 Field와의 관계를 수동으로 정의해줄 필요가 있다.
    host = TinyUserSerializer(
        read_only=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )  # array이면 many=True
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        model = House
        fields = "__all__"
        depth = 1

    def update(self, instance, validated_data):
        print(validated_data)
        return
