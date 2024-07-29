# import jwt
# from django.conf import settings
# from datetime import datetime, timedelta
# from .models import Profile
#
#
# def generate_access_token(user):
#     payload = {
#         'id': user.id,
#         'exp': datetime.utcnow() + timedelta(days=10),
#         'iat': datetime.utcnow(),
#     }
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#
#
# def generate_refresh_token(user):
#     payload = {
#         'id': user.id,
#         'exp': datetime.utcnow() + timedelta(days=180),
#         'iat': datetime.utcnow(),
#     }
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#
#
# def decode_jwt_token(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']),
#         return payload
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None


from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


def get_jwt_tokens(user):
    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)
    return (access, refresh)


def black_list_refresh_token(refresh):
    refresh_token = RefreshToken(refresh)
    refresh_token.blacklist()


def get_access_from_refresh(refresh):
    refresh = RefreshToken(refresh)
    access = str(refresh.access_token)
    return access
