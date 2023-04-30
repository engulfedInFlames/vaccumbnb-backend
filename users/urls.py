from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("change-password/", views.You.as_view()),
    path("me/", views.Me.as_view(), name="me"),
    path("me/password", views.Password.as_view()),
    # "<str:username>"이 "me"보다 위에 있게 되면, Django가 "me"를 url 주소가 아닌 username으로 인식한다. 만약 "me"라는 username의 사용자가 있다면? "@"
    path("@<str:username>/", views.You.as_view(), name="you"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view()),
    path("github-login/", views.GithubLogin.as_view()),
    path("kakao-login/", views.KakaoLogin.as_view()),
]
