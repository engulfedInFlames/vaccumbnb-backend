from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from amenities.models import Amenity
from .serializers import (
    CreateAmenitySerializer,
    AmenityListSerializer,
    AmenityDetailSerializer,
)


class AmenityList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, _):
        amenities = Amenity.objects.all()
        serializer = AmenityListSerializer(amenities, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = CreateAmenitySerializer(data=request.data)

        if serializer.is_valid():
            amenity = serializer.save(host=request.user)
            serializer = AmenityDetailSerializer(amenity)
            return Response(serializer.data, status=HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AmenityDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(Amenity, id=id)

    def get(self, _, id):
        amenity = self.get_object(id)
        serializer = AmenityDetailSerializer(amenity)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, id):
        amenity = self.get_object(id)
        serializer = AmenityDetailSerializer(amenity, data=request.data, partial=True)

        if serializer.is_valid():
            amenity = serializer.save()

            if amenity.host != request.user:
                raise PermissionDenied

            serializer = AmenityDetailSerializer(amenity)
            return Response(serializer.data, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        amenity = self.get_object(id)

        if amenity.host != request.user:
            raise PermissionDenied

        amenity.delete()

        return Response(status=HTTP_204_NO_CONTENT)
