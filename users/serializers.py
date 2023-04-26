from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CustomUser


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "name",
            "username",
            "avatar",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "avatar",
            "name",
            "gender",
            "language",
            "currency",
            "is_host",
            "last_login",
            "date_joined",
        )


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "avatar",
            "name",
            "gender",
            "language",
            "currency",
            "is_host",
            "last_login",
            "date_joined",
        )
