from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .models import Amenity
from .serializers import (
    AmenityDetailSerializer,
)


class AmenityDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Amenity, pk=pk)

    def get(self, _, pk):
        amenity = self.get_object(pk)
        serializer = AmenityDetailSerializer(amenity)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        amenity = self.get_object(pk)

        if amenity.host != request.user:
            raise PermissionDenied

        serializer = AmenityDetailSerializer(
            amenity,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            amenity = serializer.save()
            serializer = AmenityDetailSerializer(amenity)
            return Response(serializer.data, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)

        if amenity.host != request.user:
            raise PermissionDenied

        amenity.delete()
        return Response(status=HTTP_200_OK)
