from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotAuthenticated, ParseError, PermissionDenied
from .serializers import HouseListSerializer, HouseDetailSerializer, AmenitySerializer
from .models import House, Amenity
from categories.models import Category


class Houses(APIView):
    def get(self, request):
        all_houses = House.objects.all()
        serializer = HouseListSerializer(all_houses, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated
        serializer = HouseDetailSerializer(data=request.data)
        if serializer.is_valid():
            # save를 호출하면 create 또는 update가 호출되고, 각 메소드들은 validated_data를 가진다. 다른 말로, validated_data에 데이터를 추가하고 싶다면, save 함수 안에 데이터를 넣어주면 된다.
            category_id = request.data.get("category")

            if not category_id:
                raise ParseError("Category is required.")

            category = get_object_or_404(Category, id=category_id)

            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be 'houses'.")

            try:
                with transaction.atomic():  # try-except를 안에서 사용하면 transaction이 오류가 발생한지 모른다.
                    house = serializer.save(
                        host=user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")
                    for amenity_id in amenities:
                        amenity = Amenity.objects.get(id=amenity_id)
                        # Work with many to many field. Use "add" method.
                        house.amenities.add(amenity)  # <-> remove
                    serializer = HouseDetailSerializer(house)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors)


"""
{
    "id":1,
    "host": {
        "name": "admin",
        "username": "admin",
        "avatar": null
    },
    "amenities": [
        {
            "name": "Kitchen",
            "description": null
        }
    ],
    "category": {
        "name": "Penthouse",
        "kind": "houses"
    },
    "name": "A Beautiful Penthouse",
    "country": "U.S.A",
    "city": "Newyork City",
    "price": 350,
    "rooms": 7,
    "toilets": 4,
    "description": "This Penthouse is the most beautiful one in Newyork, U.S.A",
    "address": "somewhere in Newyork",
    "pet_allowed": true,
    "kind": "entire_place"
}
"""


class HouseDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(House, id=id)

    def get(self, request, id):
        house = self.get_object(id)
        serializer = HouseDetailSerializer(house)
        return Response(serializer.data)

    def put(self, request, id):
        user = request.user
        house = self.get_object(id)
        if not user.is_authenticated:
            raise NotAuthenticated
        if user != house.host:
            raise PermissionDenied

        # category validation
        category = request.data.get("category")

        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("The category kind should be 'houses'.")

        if not Category.objects.exists(name=category.name):
            raise ParseError("The category name does not exist.")

        # amenity validation
        amenities = request.data.get("amenities")
        pop_list = []
        for index, amenity in enumerate(amenities):
            if not Amenity.objects.exists(name=amenity.name):
                pop_list.append(index)

        for index in pop_list[::-1]:
            amenities.pop(index)

        try:
            with transaction.atomic():
                serializer = HouseDetailSerializer(
                    house,
                    data=request.data,
                    partial=True,
                )

                if serializer.is_valid():
                    updated_amenity = serializer.save()
                    serializer = HouseDetailSerializer(updated_amenity)
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
        except Exception:
            raise ParseError("Failed to update the house info.")

    def delete(self, request, id):
        user = request.user
        house = self.get_object(id)
        if not user.is_authenticated:
            raise NotAuthenticated
        if user == house.host:
            raise PermissionDenied
        house.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
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
            amenity = AmenitySerializer(serializer.save())
            return Response(amenity.data)


class AmenityDetail(APIView):
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
        return Response(HTTP_204_NO_CONTENT)
