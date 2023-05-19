from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Wishlist
from houses.models import House
from experiences.models import Experience
from .serializers import WishlistSerializer


class MyWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # In summary, both approaches are used to retrieve objects from a specific model, but Model.objects.all().filter() retrieves all objects first and then filters them down, while Model.objects.filter() retrieves a QuerySet that can be further filtered. Therefore, Model.objects.filter() is more efficient when we want to narrow down the results based on specific criteria.

        wishlist = Wishlist.objects.get(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=HTTP_200_OK)


class ToggleHouseOnWishlist(APIView):
    def get_wishlist(self, pk, user):
        return get_object_or_404(Wishlist, pk=pk, user=user)

    def get_house(self, pk):
        return get_object_or_404(House, pk=pk)

    def put(self, request, pk, house_pk):
        wishlist = self.get_wishlist(pk=pk, user=request.user)
        house = self.get_house(pk=house_pk)

        if wishlist.houses.filter(pk=house_pk).exists():
            wishlist.houses.remove(house)
        else:
            wishlist.houses.add(house)

        return Response(status=HTTP_200_OK)


class ToggleExperienceOnWishlist(APIView):
    def get_wishlist(self, pk, user):
        return get_object_or_404(Wishlist, pk=pk, user=user)

    def get_experience(self, pk):
        return get_object_or_404(Experience, pk=pk)

    def put(self, request, pk, experience_pk):
        wishlist = self.get_wishlist(pk=pk, user=request.user)
        experience = self.get_experience(pk=experience_pk)

        if wishlist.experiences.filter(pk=experience_pk).exists():
            wishlist.experiences.remove(experience)
        else:
            wishlist.experiences.add(experience)

        return Response(status=HTTP_200_OK)
