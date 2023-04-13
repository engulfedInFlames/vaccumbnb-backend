from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "name",
            "username",
            "avatar",
        )
