from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Experience
from users.serializers import TinyUserSerializer
from amenities.serializers import AmenityListSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class CreateExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        exclude = ("host",)


class ExperienceListSerializer(ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = SerializerMethodField()
    is_host = SerializerMethodField()

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        user = self.context.get("user")
        if user:
            return experience.host == user

    class Meta:
        model = Experience
        exclude = (
            "host",
            "category",
        )


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    amenities = AmenityListSerializer(many=True)
    photos = PhotoSerializer(many=True)

    rating = SerializerMethodField()
    is_host = SerializerMethodField()
    is_on_wishlist = SerializerMethodField()
    reviews = SerializerMethodField()

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        user = self.context.get("user")
        if user:
            return experience.host == user
        return False

    def get_reviews(self, experience):
        return experience.reviews.all().count()

    def get_is_on_wishlist(self, experience):
        user = self.context.get("user")
        if user:
            # 1. 해당 user의 wishlist를 쿼리
            # 2. 해당 wishlist에 id가 일치하는 experience를 쿼리
            is_experience_on_wishlist = Wishlist.objects.filter(
                user=user,
                experience__pk=experience.pk,
            ).exists()
            return is_experience_on_wishlist

        return False

    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = (
            "category",
            "photos",
        )
