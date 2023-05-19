from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Photo, Video


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Photo, pk=pk)

    def delete(self, request, pk):
        photo = self.get_object(pk)

        if photo.house:
            if photo.house.host != request.user:
                raise PermissionDenied

        if photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied

        photo.delete()
        return Response(status=HTTP_200_OK)


class VideoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Video, pk=pk)

    def delete(self, request, pk):
        Video = self.get_object(pk)

        if Video.house:
            if Video.house.host != request.user:
                raise PermissionDenied

        if Video.experience:
            if Video.experience.host != request.user:
                raise PermissionDenied

        Video.delete()
        return Response(status=HTTP_200_OK)
