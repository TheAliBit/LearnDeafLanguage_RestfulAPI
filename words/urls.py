from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from LDL import settings
from .views import CategoryViewSet, WordViewSet, ExamViewSet, SentenceMakerAPIView

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('words', WordViewSet, basename='words')
router.register('exam', ExamViewSet, basename='exam')

urlpatterns = [
    path('', include(router.urls)),
    path('sentence-builder/', SentenceMakerAPIView.as_view(), name='sentence-builder'),
]