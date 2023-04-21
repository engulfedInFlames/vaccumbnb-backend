from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(Photo, id=id)

    def delete(self, request, id):
        photo = self.get_object(id)

        if photo.house:
            if photo.house.host != request.user:
                raise PermissionDenied

        if photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied

        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
