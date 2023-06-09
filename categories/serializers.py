from rest_framework.serializers import ModelSerializer
from .models import Category


class CreateCatergorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )


class CategorySerializer(ModelSerializer):
    """
    Serializer Definition for Category
    """

    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "kind",
        )
        extra_kwargs = {
            "kind": {"read_only": True},
        }


""" Below is some code to get an idea of how DRF works
    
    # read_only로
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=50,
        required=True,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # ↓ 객체 또는 에러를 반환해야 한다.
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
    """
