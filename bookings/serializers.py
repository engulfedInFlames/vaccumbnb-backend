from django.utils import timezone

from rest_framework import serializers

from .models import Booking


class BookingListSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    def get_detail(self, booking):
        if booking.house:
            context = {
                "check_in": booking.check_in,
                "check_out": booking.check_out,
            }
            return context
        else:
            context = {
                "experience_time": booking.experience_time,
            }

    class Meta:
        model = Booking
        fields = (
            "pk",
            "detail",
            "guests",
        )


class BookingDetailSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    def get_detail(self, booking):
        if booking.house:
            context = {
                "check_in": booking.check_in,
                "check_out": booking.check_out,
            }
            return context
        else:
            context = {
                "experience_time": booking.experience_time,
            }

    class Meta:
        model = Booking
        fields = (
            "pk",
            "user",
            "detail",
            "guests",
        )


class CreateHouseBookingSerializer(serializers.ModelSerializer):
    # Data가 있는지 확인하고, DateField 형식에 맞는지 확인한다.
    # DateField()로 선언했기 때문에 "date" 타입이 된다.
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # 특정 field의 validation 메소드를 만들고 싶을 때는 validate_field_name으로 선언하면 된다.
    def validate_check_in(self, value):
        now = timezone.now().date()
        if now > value:
            raise serializers.ValidationError("체크인 날짜가 이미 지났습니다.")
        return value

    def validate_check_out(self, value):
        now = timezone.now().date()
        if now > value:
            raise serializers.ValidationError("체크아웃 날짜가 이미 지났습니다.")
        return value

    # field_name을 쓰지 않았을 때는 모든 데이터를 가지고 온다
    def validate(self, values):
        if values["check_in"] >= values["check_out"]:
            raise serializers.ValidationError("체크아웃 날짜가 체크인 날짜보다 빠릅니다.")

        if Booking.objects.filter(
            check_in__lt=values["check_out"],
            check_out__gte=values["check_in"],
        ).exists():
            raise serializers.ValidationError("해당 날짜에 이미 예약이 있습니다.")

        return values

    def create(self, validated_data):
        booking = super().create(validated_data)
        booking.experience = None
        booking.save()
        return booking


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.TimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.now().date()
        if now > value:
            raise serializers.ValidationError("체크인 날짜가 이미 지났습니다.")
        return value

    def validate_check_out(self, value):
        now = timezone.now().date()
        if now > value:
            raise serializers.ValidationError("체크아웃 날짜가 이미 지났습니다.")
        return value

    # field_name을 쓰지 않았을 때는 모든 데이터를 가지고 온다
    def validate(self, values):
        if values["check_in"] >= values["check_out"]:
            raise serializers.ValidationError("체크아웃 날짜가 체크인 날짜보다 빠릅니다.")

        if Booking.objects.filter(
            check_in__lt=values["check_out"],
            check_out__gte=values["check_in"],
        ).exists():
            raise serializers.ValidationError("해당 날짜에 이미 예약이 있습니다.")

        return values

    def create(self, validated_data):
        booking = super().create(validated_data)
        booking.house = None
        booking.save()
        return booking
