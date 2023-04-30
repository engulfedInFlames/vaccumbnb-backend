from time import sleep
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import House, Amenity
from .serializers import HouseListSerializer, HouseDetailSerializer, AmenitySerializer

from categories.models import Category
from bookings.models import Booking
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.serializers import PublicBookingSerializer, CreateHouseBookingSerializer


class Houses(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_houses = House.objects.all()
        context = {"user": request.user}
        serializer = HouseListSerializer(
            all_houses,
            many=True,
            context=context,
        )
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = HouseDetailSerializer(data=request.data)

        if serializer.is_valid():
            category_id = request.data.get("category")

            if not category_id:
                raise ParseError("Category is required.")

            category = get_object_or_404(Category, id=category_id)

            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be 'houses'.")

            print("Category Validation")
            try:
                with transaction.atomic():  # try-except를 안에서 사용하면 transaction이 오류가 발생한지 모른다.
                    house = serializer.save(
                        host=user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")

                    if amenities is not None:
                        for amenity_id in amenities:
                            amenity = Amenity.objects.get(id=amenity_id)
                            # Work with many to many field. Use "add" method.
                            house.amenities.add(amenity)  # <-> remove
                    serializer = HouseDetailSerializer(house)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def get(self, request, id):
        sleep(2)
        house = self.get_object(id)
        context = {"user": request.user}
        # context로 동적 필드를 정의할 수 있다.
        serializer = HouseDetailSerializer(house, context=context)
        return Response(serializer.data)

    def put(self, request, id):
        user = request.user
        house = self.get_object(id)

        # user validation
        if user != house.host:
            raise PermissionDenied

        try:
            with transaction.atomic():
                serializer = HouseDetailSerializer(
                    house,
                    data=request.data,
                    partial=True,
                )
                if serializer.is_valid():
                    # category validation
                    category_id = request.data.get("category")
                    category = get_object_or_404(Category, id=category_id)

                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'houses'.")

                    # amenity validation
                    amenities = request.data.get("amenities")
                    house.amenities.clear()
                    for amenity_id in amenities:
                        if Amenity.objects.all().filter(id=amenity_id).exists():
                            amenity = get_object_or_404(Amenity, id=amenity_id)
                            house.amenities.add(amenity)

                    # save
                    updated_amenity = serializer.save(category=category)
                    serializer = HouseDetailSerializer(updated_amenity)
                    return Response(serializer.data)
        except Exception:
            raise ParseError("Failed to update the house info.")

    def delete(self, request, id):
        user = request.user
        house = self.get_object(id)

        if user == house.host:
            raise PermissionDenied
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HouseReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def get(self, request, id):
        # 다음의 try - except문을 잘 이해해볼 것
        page_size = settings.PAGE_SIZE
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
            if page < 1:
                raise ValueError("Negative indexing error")
            page_start = (page - 1) * 3
            page_end = page_start + page_size
        except ValueError:
            page = 1
            page_start = 0
            page_end = page_start + page_size

        house = self.get_object(id)
        serializer = ReviewSerializer(
            house.reviews.all()[page_start:page_end],  # 0 <= x < 3
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, id):
        house = self.get_object(id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                house=house,
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class HouseAmenities(APIView):
    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def get(self, request, id):
        # 다음의 try - except문을 잘 이해해볼 것
        page_size = 3
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
            if page < 1:
                raise ValueError("Negative indexing error")
            page_start = (page - 1) * 3
            page_end = page_start + page_size
        except ValueError:
            page = 1
            page_start = 0
            page_end = page_start + page_size

        house = self.get_object(id)
        serializer = AmenitySerializer(
            house.amenities.all()[page_start:page_end],
            many=True,
        )
        return Response(serializer.data)


class Amenities(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request.data에는 어떤 데이터들이?
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            # save()는 내부 메소드 create, 또는 update를 호출하고 객체를 반환한다.
            # 브라우저에서 읽기 쉬해서는 JSON Encoded가 필요!
            amenity = serializer.save()
            serializer = AmenitySerializer(amenity)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Amenity, id=id)

    def get(self, request, id):
        amenity = self.get_object(id)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, id):
        amenity = self.get_object(id)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_serializer = AmenitySerializer(serializer.save())
            return Response(updated_serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        amenity = self.get_object(id)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HousePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def post(self, request, id):
        house = self.get_object(id)

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

    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def get(self, request, id):
        """
        The Other Option
        bookings = Booking.objects.filter(house__id=id)
        DB를 두 번 조회할 필요가 없다. 하지만 조회하려는 방이 없을 때나 방에 예약이 없을 때나 빈 QuerySet이라는 같은 결과를 반환하여 구분할 수 없게 된다.

        """

        """
        월별 혹은 연도별로 조회할 수 있게 하려면?
        # 11.23
        """

        house = self.get_object(id)
        now = timezone.now().date()
        bookings = Booking.objects.filter(
            house=house,
            kind=Booking.BookingKindChoices.HOUSE,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        house = self.get_object(id)
        serializer = CreateHouseBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                house=house,
                kind=Booking.BookingKindChoices.HOUSE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
