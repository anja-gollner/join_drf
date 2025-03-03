from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer, EmailLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework import status


# class UserProfileList(generics.ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


# class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
        else:
            data = serializer.errors

        return Response(data)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)

        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            return Response({"error": "E-Mail-Adresse ist nicht registriert."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                'full_name': user.first_name,
                "username": user.username,
                "email": user.email,
            })

        return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)


class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            guest_user, created = User.objects.get_or_create(username="Guest")
            token, created = Token.objects.get_or_create(user=guest_user)

            return Response({
                "token": token.key,
                "username": guest_user.username,
                "email": guest_user.email if guest_user.email else "",
            })
        except Exception as e:
            return Response({"error": "Guest login failed."}, status=status.HTTP_400_BAD_REQUEST)


class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"error": "Diese E-Mail-Adresse ist bereits registriert."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "E-Mail verfügbar"}, status=status.HTTP_200_OK)
