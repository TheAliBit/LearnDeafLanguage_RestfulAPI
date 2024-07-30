from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from .models import Category, Word
from .serializers.category_serializers import CategorySerializer
from .serializers.word_list_and_details import WordSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent']


class WordViewSet(ModelViewSet):
    queryset = Word.objects.prefetch_related('category').all()
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']
