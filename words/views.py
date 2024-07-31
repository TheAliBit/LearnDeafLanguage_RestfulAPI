import random

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Word
from .serializers.category_serializers import CategorySerializer
from .serializers.word_list_and_details import WordSerializer, EmptySerializer, SimpleWordSerializer
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

    # liking and unliking the word
    @action(detail=True, methods=['post'], url_path='like-and-unlike', serializer_class=EmptySerializer)
    def like_unlike(self, request, pk=None):
        word = get_object_or_404(Word, pk=pk)
        profile = request.user

        if word in profile.liked_words.all():
            profile.liked_words.remove(word)
            return Response({'کلمه با موفقیت از لیست علاقه مندی ها حذف شد!'}, status=status.HTTP_200_OK)
        else:
            profile.liked_words.add(word)
            return Response({'کلمه با موفقیت به لیست علاقه مندی ها اضافه شد!'}, status=status.HTTP_200_OK)


# writing the exam APIView
class ExamViewSet(ViewSet):
    def get(self, request):
        # ordering objects in a random order and slice the first 4
        words = Word.objects.order_by('?')[:4]

        # serializing the word instances
        serializer = SimpleWordSerializer(words, many=True)

        response_data = {
            "exam": serializer.data,
            "correct_word": random.choices(serializer.data)
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request):
        correct_word_id = request.data.get('correct_word_id')
        chosen_word_id = request.data.get('chosen_word_id')

        if chosen_word_id == correct_word_id:
            return Response({"درست گفتی!"}, status=status.HTTP_200_OK)
        else:
            return Response({"اشتباه گفتی!"}, status=status.HTTP_200_OK)
