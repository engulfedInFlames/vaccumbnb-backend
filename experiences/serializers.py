from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Experience


class CreateExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    category = SerializerMethodField()

    def get_category(self, house):
        return house.category

    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ("category",)
