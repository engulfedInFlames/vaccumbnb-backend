from django.shortcuts import render
from .models import House
from django.http import HttpResponse


# views.py에서는 특정 url에 대한 request를 처리하는 함수를 정의한다.
def say_hello(request):
    # 일반 str을 반환해서는 안 된다. HTTP response를 반환해야 한다.
    return HttpResponse("Hello!")


def all_houses(request):
    houses = House.obejcts.all()
    return HttpResponse("All Houses")


def only_one_house(request, _id):
    try:
        house = House.objects.get(pk=_id)
        return HttpResponse("Only One House")
    except House.DoesNotExist:
        return HttpResponse(f"Failed to get house_id : {_id}")
