from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, WordViewSet, ExamViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('words', WordViewSet)
router.register('exam', ExamViewSet, basename='exam')
# router.register('sentence-builder', ...)

urlpatterns = [
    path('', include(router.urls))
]
