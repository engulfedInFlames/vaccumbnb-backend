from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .models import Booking
from .serializers import BookingDetailSerializer


class BookingDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Booking, pk=pk)

    def get(self, request, pk):
        booking = self.get_object(pk)
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        booking = self.get_object(pk)

        if booking.host != request.user:
            raise PermissionDenied

        serializer = BookingDetailSerializer(
            booking,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            booking = serializer.save()
            serializer = BookingDetailSerializer(booking)
            return Response(serializer.data, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = self.get_object(pk)

        if booking.host != request.user:
            raise PermissionDenied

        booking.delete()
        return Response(status=HTTP_200_OK)
