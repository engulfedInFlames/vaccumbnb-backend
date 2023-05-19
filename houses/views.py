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

from .models import House
from . import serializers

from amenities.models import Amenity
from categories.models import Category
from bookings.models import Booking
from amenities.serializers import AmenityListSerializer
from reviews import serializers as reviewSerializers
from medias.serializers import PhotoSerializer
from bookings.serializers import BookingListSerializer, CreateHouseBookingSerializer


class Houses(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_houses = House.objects.all()
        context = {"user": request.user}
        serializer = serializers.HouseListSerializer(
            all_houses,
            many=True,
            context=context,
        )
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = serializers.CreateHouseSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")

            if not category_pk:
                raise ParseError("Category is required.")

            category = get_object_or_404(Category, pk=category_pk)

            if category.kind == Category.CategoryKindChoices.HOUSES:
                raise ParseError("The category kind should be 'houses'.")

            try:
                with transaction.atomic():  # try-except를 안에서 사용하면 transaction이 오류가 발생한지 모른다.
                    house = serializer.save(
                        host=user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")

                    for amenity_pk in amenities:
                        amenity = get_object_or_404(Amenity, pk=amenity_pk)
                        house.amenities.add(amenity)  # <-> remove
                    serializer = serializers.HouseDetailSerializer(house)
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(House, pk=pk)

    def get(self, request, pk):
        sleep(0.5)
        house = self.get_object(pk)
        context = {"user": request.user}
        serializer = serializers.HouseDetailSerializer(house, context=context)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        house = self.get_object(pk)

        if user != house.host:
            raise PermissionDenied

        try:
            with transaction.atomic():
                amenities = request.data.pop("amenities", None)
                house.amenities.clear()
                for amenity_pk in amenities:
                    if Amenity.objects.filter(pk=amenity_pk).exists():
                        amenity = get_object_or_404(Amenity, pk=amenity_pk)
                        house.amenities.add(amenity)

                serializer = serializers.HouseDetailSerializer(
                    house,
                    data=request.data,
                    partial=True,
                )

                if serializer.is_valid():
                    house = serializer.save()
                    serializer = serializers.HouseDetailSerializer(house)

                    return Response(serializer.data, status=status.HTTP_200_OK)

                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception:
            raise ParseError("Failed to update the house info.")

    def delete(self, request, pk):
        house = self.get_object(pk)

        if request.user != house.host:
            raise PermissionDenied

        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HouseReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(House, pk=pk)

    def get(self, request, pk):
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

        house = self.get_object(pk)
        serializer = reviewSerializers.ReviewListSerializer(
            house.reviews.all()[page_start:page_end],  # 0 <= x < 3
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        house = self.get_object(pk)
        serializer = reviewSerializers.CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                house=house,
            )
            serializer = reviewSerializers.ReviewDetailSerializer(review)
            return Response(serializer.data)


class HouseAmenities(APIView):
    def get(self, request, pk):
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

        house = get_object_or_404(House, pk=pk)
        serializer = AmenityListSerializer(
            house.amenities.all()[page_start:page_end],
            many=True,
        )

        return Response(serializer.data)


class HousePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(House, pk=pk)

    def post(self, request, pk):
        house = self.get_object(pk)

        if request.user != house.host:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            # save에 인자를 넣어 cleaned_data에 데이터를 추가할 수 있다.
            photo = serializer.save(house=house)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class HouseBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(House, pk=pk)

    def get(self, request, pk):
        """
        The Other Option
        bookings = Booking.objects.filter(house__pk=pk)
        DB를 두 번 조회할 필요가 없다. 하지만 조회하려는 방이 없을 때나 방에 예약이 없을 때나 빈 querySet이 되어 같은 결과를 반환하므로, 구분할 수 없게 된다.
        """

        """
        월별 혹은 연도별로 조회할 수 있게 하려면?
        # 11.23
        """

        house = self.get_object(pk)
        now = timezone.now().date()
        bookings = Booking.objects.filter(
            house=house,
            kind=Booking.BookingKindChoices.HOUSE,
            check_in__gt=now,
        )
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        house = self.get_object(pk)
        serializer = CreateHouseBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                house=house,
                kind=Booking.BookingKindChoices.HOUSE,
            )
            serializer = BookingListSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
