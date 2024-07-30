# from django.urls import path
# from .views import signup, login, logout, refresh_token, protected_view
#
# urlpatterns = [
#     path('signup/', signup, name='signup'),
#     path('login/', login, name='login'),
#     path('logout/', logout, name='logout'),
#     path('refresh-token/', refresh_token, name='refresh_token'),
#     path('protected/', protected_view, name='protected_view'),
# ]

from django.urls import path
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, RefreshAPIView, ProfileView, SetPremiumView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('set_premium/', SetPremiumView.as_view(), name='set_premium'),

]
