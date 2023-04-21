from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from .models import Wishlist
from houses.models import House
from .serializers import WishlistSerializer


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # In summary, both approaches are used to retrieve objects from a specific model, but Model.objects.all().filter() retrieves all objects first and then filters them down, while Model.objects.filter() retrieves a QuerySet that can be further filtered. Therefore, Model.objects.filter() is more efficient when we want to narrow down the results based on specific criteria.

        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        return get_object_or_404(Wishlist, id=id, user=user)

    def get(self, request, id):
        wishlist = self.get_object(id, request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def delete(self, request, id):
        wishlist = self.get_object(id, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, id):
        wishlist = self.get_object(id, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class WishlistFlipper(APIView):
    def get_wishlist(self, id, user):
        return get_object_or_404(Wishlist, id=id, user=user)

    def get_house(self, id):
        return get_object_or_404(House, id=id)

    def put(self, request, id, house_id):
        wishlist = self.get_wishlist(id=id, user=request.user)
        house = self.get_house(id=house_id)

        if wishlist.houses.filter(id=house.id).exists():
            wishlist.houses.remove(house)
        else:
            wishlist.houses.add(house)

        return Response(status=HTTP_200_OK)
