from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, bad_request, NotAuthenticated
from rest_framework import status
import requests

from .models import CustomUser
from . import serializers


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class You(APIView):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        serializer = serializers.PrivateUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Users(APIView):
    def post(self, request):
        """Password Validation"""

        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        try:
            validate_password(password)
        except Exception as e:
            raise ParseError(e)

        serializer = serializers.PrivateUserSerializer(data=request.data)

        # username의 중복 검사 등을 serializer가 대신 수행한다!
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Login(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # authenticate 메소드는 username과 password의 일치 여부를 반환한다.
        username = request.data.get("username")
        password = request.data.get("password")

        if not all([username, password]):
            raise ParseError("Username and password are all required.")

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # django는 유저를 로그인시키고, 백엔드에서 유저 정보가 담긴 세션을 생성하고, 유저에게 쿠키를 전달한다.
            login(request, user)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response("logout", status=status.HTTP_200_OK)


class Password(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        """ Password Validation """

        try:
            validate_password(current_password)
            validate_password(new_password)
        except Exception as e:
            raise ParseError(e)

        if not all([current_password, new_password]):
            return ParseError("Current password and new password are all required.")

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError("Not Correct Password")


class GithubLogin(APIView):
    def post(self, request):
        try:
            # code는 한 번만 사용할 수 있다. REACT는 개발 모드에서 스크린을 두 번 렌더링한다.
            code = request.data.get("code")
            response = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GITHUB_CLIENT_ID}&client_secret={settings.GITHUB_CLIENT_SECRET}",
                headers={"Accept": "application/json"},
            )
            # print(response.json())
            access_token = response.json().get("access_token")
            response = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = response.json()
            # print(user_data)

            """
            깃허브로부터 받은 email 리스트가 장고 DB에 있으면 로그인, 없으면 회원가입이라고 유추할 수 있다.
            """

            response = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = response.json()

            user_email = None
            for email in user_emails:
                if email.get("primary") and email.get("verified"):
                    user_email = email

            if user_email is None:
                raise bad_request

            try:
                user = CustomUser.objects.get(email=user_email.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                user = (
                    CustomUser.objects.create_user(
                        # username은 unique함에 유의하자
                        username=user_data.get("login"),
                        email=user_email.get("email"),
                        name=user_data.get("name", ""),
                        avatar=user_data.get("avatar_url"),
                    ),
                )
                user.set_unusable_password()
                # has_usable_password()는 유저의 password가 usable인지 확인한다.
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "39669f9889ada8c1d0b149f32dfa7c20",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao/",
                    "code": code,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                },
            )
            access_token = response.json().get("access_token")
            response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = response.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")

            if not kakao_account.get("is_email_verified"):
                raise NotAuthenticated

            try:
                user = CustomUser.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                user = (
                    CustomUser.objects.create_user(
                        # username은 unique함에 유의하자
                        username=profile.get("nickname"),
                        email=kakao_account.get("email"),
                        name=profile.get("nickname"),
                        avatar=profile.get("profile_image_url"),
                    ),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
