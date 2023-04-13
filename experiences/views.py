from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            serializer = PerkSerializer(serializer.save())
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Perk, id=id)

    def get(self, request, id):
        serializer = PerkSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, id):
        serializer = PerkSerializer(
            self.get_object(id),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = PerkSerializer(serializer.save())
            return Response(updated_perk.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        perk = self.get_object(id)
        perk.delete()
        return Response(HTTP_204_NO_CONTENT)
