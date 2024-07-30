# from django.contrib.auth import authenticate, login as django_login, logout as django_logout
# from django.http import JsonResponse
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
#
# from .authentication import JWTAuthentication
# from .utils import generate_access_token, generate_refresh_token, decode_jwt_token
# from .models import Profile
# from .serializers import RegisterSerializer, ProfileSerializer
# from rest_framework.response import Response
#
#
# @csrf_exempt
# @api_view(['POST'])
# def signup(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
#
#     if user is not None:
#         django_login(request, user)
#         access_token = generate_access_token(user)
#         refresh_token = generate_refresh_token(user)
#         return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     django_logout(request)
#     return JsonResponse({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['POST'])
# def refresh_token(request):
#     refresh_token = request.data.get('refresh_token')
#     payload = decode_jwt_token(refresh_token)
#
#     if payload:
#         try:
#             user = Profile.objects.get(id=payload['id'])
#         except Profile.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         new_access_token = generate_access_token(user)
#         return JsonResponse({'access_token': new_access_token}, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({'error': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def protected_view(request):
#     serializer = ProfileSerializer(request.user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
#
# from .serializers import UserSerializer
#
# from .models import Profile
#
# import jwt, datetime
#
#
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     """
#        from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
#
#        serializer -> validate(username, password)
#        serializer.is_valid()
#
#        user
#        AccessToken.for_user(user)
#        RefreshToken.for_user(user)
#        Response({'access': x, 'refresh': y})
#
#        "0919 153 8289".strip()
#        """
#
#
# class LoginView(APIView):
#
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#         user = Profile.objects.filter(username=username).first()
#         if user is None:
#             raise AuthenticationFailed('User not found!')
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')
#         payload = {
#             'id': user.id,
#             'username': str(user.username).strip(),
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
#             'iat': datetime.datetime.utcnow(),
#         }
#         token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
#         return Response({
#             'jwt': token
#         })

# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.permissions import IsAuthenticated
# from django.db import transaction
# from django.core.cache import cache
# from .serializers import LoginSerializer, RefreshSerializer
#
#
# class LoginAPIView(generics.CreateAPIView):
#     serializer_class = LoginSerializer
#
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#     try:
#         access, refresh = login_user(serializer.data['phone_number'], serializer.data['code'])
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#     response = Response(data={'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)
#     response.set_cookie('access', access, httponly=True, expires=10 * 60)
#     response.set_cookie('refresh', refresh, httponly=True, expires=180 * 60 * 60 * 24)
#     return response


from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .serializers.registration_serializers import SignupSerializer, LoginSerializer, RefreshSerializer
from .serializers.Profile_serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from .utils import black_list_refresh_token, get_access_from_refresh  # Ensure these utility functions are imported
from core.models  import Profile


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
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

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
