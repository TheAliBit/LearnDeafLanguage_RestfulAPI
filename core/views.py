from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .serializers.registration_serializers import SignupSerializer, LoginSerializer, RefreshSerializer
from .serializers.Profile_serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from .utils import black_list_refresh_token, get_access_from_refresh
from core.models import Profile


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'ثبت نام با موفقیت انجام شد!'}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['phone_number'],
                            password=serializer.validated_data['password'])
        if not user:
            return Response({'error': 'شماره تلفن یا رمز عبور اشتباه است!'}, status=status.HTTP_400_BAD_REQUEST)

        access = str(AccessToken.for_user(user))
        refresh = str(RefreshToken.for_user(user))
        return Response(data={'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        black_list_refresh_token(serializer.data['refresh'])
        return Response(data={'message': 'با موفقیت خارج شدید!'}, status=status.HTTP_200_OK)


class RefreshAPIView(generics.CreateAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = get_access_from_refresh(serializer.data['refresh'])
        return Response(data={'access': access}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


# here i add the view for change the user to premium
class SetPremiumView(APIView):
    permission_classes = [IsAuthenticated]

    # for changing a user membershib and etc we should use post method not get or anything else
    def post(self, request):
        try:
            user_profile = Profile.objects.get(id=request.user.id)
            user_profile.membership = True
            user_profile.save()
            return Response({"message": "به کار طلایی تبدیل شدید!"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error:": "چنین کاربری وجود ندارد!"})
