from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .models import Review
from .serializers import ReviewDetailSerializer


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Review, pk=pk)

    def get(self, _, pk):
        review = self.get_object(pk)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        review = self.get_object(pk)

        if review.host != request.user:
            raise PermissionDenied

        serializer = ReviewDetailSerializer(
            review,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            review = serializer.save(user=request.user)
            serializer = ReviewDetailSerializer(review)
            return Response(serializer.data, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)

        if review.host != request.user:
            raise PermissionDenied

        review.delete()
        return Response(status=HTTP_200_OK)
