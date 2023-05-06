from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Amenity


class CreateAmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "detail",
            "description",
            "parent",
        )

    def create(self, validated_data):
        amenity = super().create(validated_data)

        if amenity.parent == "house" and amenity.description:
            amenity.description = None

        amenity.save()

        return amenity


class AmenityListSerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "detail",
            "description",
            "parent",
        )


class AmenityDetailSerializer(ModelSerializer):
    host = SerializerMethodField()

    def get_host(self, amenity):
        return amenity.host.name

    class Meta:
        model = Amenity
        fields = (
            "id",
            "name",
            "detail",
            "description",
            "parent",
            "host",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("parent",)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
