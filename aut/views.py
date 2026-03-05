from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from . import models as m
from core import utils

User = get_user_model()
OTP_EXPIRY_SECONDS = 300

class LoginOTPAPIView(APIView):
  permission_classes = (permissions.AllowAny,)
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(request, username=serializer.validated_data["username"], password=serializer.validated_data["password"])
    if not user: return Response({"status": False, "message": "Username or password is incorrect."}, status=401)
    data = UserSerializer(user).data
    login(request, user)
    return Response({"status": True, "data": data, "tokens": utils.getUserTokens(user)})

class RegisterAPIView(APIView):
  permission_classes = (permissions.AllowAny,)
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"status": True, "message": "User created Successfully"}, status=status.HTTP_201_CREATED)

class LogoutAPIView(APIView):
  permission_classes = (permissions.IsAuthenticated,)
  def post(self, request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
