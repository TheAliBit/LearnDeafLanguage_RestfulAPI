from django.conf.urls.static import static
from django.urls import path

from LDL import settings
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, RefreshAPIView, ProfileView, SetPremiumView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('set_premium/', SetPremiumView.as_view(), name='set_premium'),
]
