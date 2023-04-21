from rest_framework.serializers import ModelSerializer
from .models import Review
from users.serializers import TinyUserSerializer


class ReviewSerializer(ModelSerializer):
    # request.data에 user 데이터가 없어도 serializer가 유효하기 위해서 read_only=True로 설정한다.
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
