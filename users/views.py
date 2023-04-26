from django.shortcuts import render, get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status

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
