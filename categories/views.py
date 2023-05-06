from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


# ModelViewSet을 사용해야 할 때와 APIView로 Custom View를 사용해야 할 때를 구분할 줄 알아야 한다.


class HouseCategoryViewSet(ModelViewSet):
    # ModelViewSet은 1. serializer, 2 ViewSet의 object, 두 가지를 알아야 한다.

    serializer_class = CategorySerializer
    queryset = Category.objects.all().filter(kind="houses")


class ExperienceCategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().filter(kind="experiences")


""" Below is some code to get an idea of how the decorator 'api_view' works

from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

@api_view(["GET", "POST"])
def all_categories(request):
    # 브라우저는 queryset을 이해 X, JSON 형식으로 변환해야 한다.
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        context = {
            "ok": True,
            "categories": serializer.data,
        }

        return Response(context)

    if request.method == "POST":
        # JSON to Django : request 데이터를 Date 키워드의 인자로
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # ↓ 호출되면 자동으로 serializer 내의 create 메소드를 호출한다.
            # ↓ create 메소드 내에서 객체의 데이터를 저장하는 것은 개발자의 몫
            new_category = serializer.save()
            return Response(CategorySerializer(new_category.data))
        else:
            print("Invalid")
            return Response({"post": "posted"})

    return redirect("/")


@api_view(["GET", "PUT", "DELETE"])
def one_category(request, _id):
    try:
        category = Category.objects.get(pk=_id)
    except Category.DoesNotExist:
        # raise 되면 그 이후의 코드들은 실행 X
        raise NotFound

    if request.method == "GET":
        # Django to JSON : 객체를 인자로
        serializer = CategorySerializer(category)
        context = {
            "ok": True,
            "category": serializer.data,
        }
        return Response(context)

    if request.method == "PUT":
        # serializer는 category의 모양을 알고 있기 때문에, 갱신할 category 객체를 인자로 넘기기만 하면 된다.
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,  # serializer에게 부분만 변경, 즉, 갱신할 것임을 알림.
        )
        if serializer.is_valid():
            # partial=True 이므로, serializer는 create가 아닌 update 메소드를 호출
            # serializer의 save 메소드는 Model의 save 메소드와 다르다. 상황에 따라 어떤 함수를 호출할 것인지를 결정한다.
            updated_category = CategorySerializer(serializer.save())
            return Response(updated_category.data)
        else:
            return Response(serializer.errors)

    if request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_202_ACCEPTED)

    return redirect(f"/categoreis/{_id}")
"""
