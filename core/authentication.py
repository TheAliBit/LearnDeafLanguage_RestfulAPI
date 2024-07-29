# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from .utils import decode_jwt_token
# from .models import Profile
#
#
# class JWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth = request.headers.get('Authorization', None)
#         if not auth:
#             return None
#
#         try:
#             prefix, token = auth.split(' ')
#             if prefix != 'Bearer':
#                 raise AuthenticationFailed('Invalid token prefix')
#         except ValueError:
#             raise AuthenticationFailed('Invalid Authorization header format')
#
#         payload = decode_jwt_token(token)
#         if not payload:
#             raise AuthenticationFailed('Invalid or expired token')
#
#         try:
#             user = Profile.objects.get(id=payload['id'])
#         except Profile.DoesNotExist:
#             raise AuthenticationFailed('User not found')
#
#         return (user, token)
#
#     def authenticate_header(self, request):
#         return 'Bearer'
