from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from core import utils

User = get_user_model()

class LoginOTPAPIView(APIView):
  permission_classes = (permissions.AllowAny,)
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    if data["loginWay"] == "email": user = authenticate(request, email=data["email"], password=data["password"])
    else: user = authenticate(request, username=data["username"], password=data["password"])
    if not user: return Response({"status": False, "message": "Username or password is incorrect."}, status=401)
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
