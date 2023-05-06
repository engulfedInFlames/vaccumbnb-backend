from time import sleep
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Experience
from .serializers import (
    CreateExperienceSerializer,
    ExperienceListSerializer,
    ExperienceDetailSerializer,
)

from amenities.models import Amenity
from categories.models import Category
from bookings.models import Booking
from amenities.serializers import AmenityListSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)


class ExperienceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        context = {"user": request.user}
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
            context=context,
        )
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = CreateExperienceSerializer(data=request.data)

        if serializer.is_valid():
            category_id = request.data.get("category")

            if not category_id:
                raise ParseError("Category is required.")

            category = get_object_or_404(Category, id=category_id)

            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be 'experiences'.")

            try:
                with transaction.atomic():  # try-except를 안에서 사용하면 transaction이 오류가 발생한지 모른다.
                    experience = serializer.save(
                        host=user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")

                    if amenities is not None:
                        for amenity_id in amenities:
                            amenity = get_object_or_404(Amenity, id=amenity_id)
                            experience.amenities.add(amenity)
                    serializer = ExperienceDetailSerializer(experience)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Experience, id=id)

    def get(self, request, id):
        sleep(0.5)
        experience = self.get_object(id)
        context = {"user": request.user}
        # context로 동적 필드를 정의할 수 있다.
        serializer = ExperienceDetailSerializer(experience, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = request.user
        house = self.get_object(id)

        # user validation
        if user != house.host:
            raise PermissionDenied

        try:
            with transaction.atomic():
                amenities = request.data.pop("amenities", None)
                experience.amenities.clear()
                for amenity_id in amenities:
                    if Amenity.objects.filter(id=amenity_id).exists():
                        amenity = get_object_or_404(Amenity, id=amenity_id)
                        experience.amenities.add(amenity)

                serializer = ExperienceDetailSerializer(
                    experience,
                    data=request.data,
                    partial=True,
                )

                if serializer.is_valid():
                    experience = serializer.save()
                    serializer = ExperienceDetailSerializer(experience)

                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception:
            raise ParseError("Failed to update the experience info.")

    def delete(self, request, id):
        house = self.get_object(id)

        if request.user != house.host:
            raise PermissionDenied

        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Experience, id=id)

    def get(self, request, id):
        page_size = settings.PAGE_SIZE

        try:
            page = request.query_params.get("page", 1)
            page = int(page)

            if page < 1:
                raise ValueError("Negative indexing error")
            page_start = (page - 1) * page_size
            page_end = page_start + page_size

        except ValueError:
            page_start = 0
            page_end = page_start + page_size

        experience = self.get_object(id)
        serializer = ReviewSerializer(
            experience.reviews.all()[page_start:page_end],  # 0 <= x < 3
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, id):
        experience = self.get_object(id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                house=experience,
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceAmenities(APIView):
    def get(self, request, id):
        page_size = settings.PAGE_SIZE

        try:
            page = request.query_params.get("page", 1)
            page = int(page)

            if page < 1:
                raise ValueError("Negative indexing error")

            page_start = (page - 1) * page_size
            page_end = page_start + page_size

        except ValueError:
            page_start = 0
            page_end = page_start + page_size

        experience = get_object_or_404(Experience, id=id)
        serializer = AmenityListSerializer(
            experience.amenities.all()[page_start:page_end],
            many=True,
        )

        return Response(serializer.data)


class ExperiencePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Experience, id=id)

    def post(self, request, id):
        experience = self.get_object(id)

        if request.user != experience.host:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            # save에 인자를 넣어 cleaned_data에 데이터를 추가할 수 있다.
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Experience, id=id)

    def get(self, request, id):
        experience = self.get_object(id)
        now = timezone.now().date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        experience = self.get_object(id)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""
