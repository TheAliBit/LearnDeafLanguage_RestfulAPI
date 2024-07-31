from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, WordViewSet, ExamViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'words', WordViewSet)
router.register(r'exam', ExamViewSet, basename='exam')

urlpatterns = [
    path('', include(router.urls))
]
