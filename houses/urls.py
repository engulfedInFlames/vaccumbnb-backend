from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello, name="say_hello"),
    path('all', views.all_houses, name="all_houses"),
    path('<int:_id>', views.only_one_house, name="only_one_house"),
]
