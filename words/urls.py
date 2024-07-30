from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, WordViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'words', WordViewSet)

urlpatterns = [
    path('', include(router.urls))
]
