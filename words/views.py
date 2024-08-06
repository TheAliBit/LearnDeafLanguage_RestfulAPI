import random
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Word
from .serializers.category_serializers import CategorySerializer
from .serializers.word_list_and_details import WordSerializer, EmptySerializer, SimpleWordSerializer, \
    VSimpleWordSerializer, PremiumWordSerializer, SimpleWordSerializerWithVideo


# TODO: add permissions for views
class CategoryViewSet(ModelViewSet):
    # TODO: return parent none categories when no filter applied
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    filterset_fields = ['parent']

    def get_queryset(self):
        queryset = super().get_queryset()
        parent_param = self.request.query_params.get('parent', None)
        if parent_param is None:
            queryset = queryset.filter(parent__isnull=True)
        return queryset


class WordViewSet(ModelViewSet):
    queryset = Word.objects.order_by('id')
    filterset_fields = ['category']
    search_fields = ['title']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        profile = self.request.user
        is_premium = profile.membership
        if is_premium:
            return PremiumWordSerializer
        return WordSerializer

    @action(detail=True, methods=['post'], url_path='like-and-unlike', serializer_class=EmptySerializer)
    def like_unlike(self, request, pk=None):
        word = get_object_or_404(Word, pk=pk)
        profile = request.user

        if word in profile.liked_words.all():
            profile.liked_words.remove(word)
            return Response({'message': 'کلمه با موفقیت از لیست علاقه مندی ها حذف شد!'}, status=status.HTTP_200_OK)
        else:
            profile.liked_words.add(word)
            return Response({'message': 'کلمه با موفقیت به لیست علاقه مندی ها اضافه شد!'}, status=status.HTTP_200_OK)


class ExamViewSet(ViewSet):
    def list(self, request):
        word_ids = Word.objects.values_list('id', flat=True)
        random_ids = random.sample(list(word_ids), 4)
        random_words = Word.objects.filter(id__in=random_ids)
        serializer = SimpleWordSerializer(random_words, many=True)

        response_data = {
            "exam": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PremiumExamViewSet(ViewSet):
    def list(self, request):
        profile = request.user
        is_premium = profile.membership
        if not (is_premium):
            return Response({'message': '!برای دسترسی به این بخش باید کاربر ویژه باشید'},
                            status=status.HTTP_403_FORBIDDEN)
        word_ids = Word.objects.values_list('id', flat=True)
        random_ids = random.sample(list(word_ids), 4)
        random_words = Word.objects.filter(id__in=random_ids)
        serializer = SimpleWordSerializerWithVideo(random_words, many=True)
        response_data = {
            "exam": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SentenceMakerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        word_ids = request.data.get('ids')
        if not word_ids or not isinstance(word_ids, list):
            return Response({'error': 'A list of IDs is required'}, status=status.HTTP_400_BAD_REQUEST)
        words = Word.objects.filter(id__in=word_ids)
        serializer = VSimpleWordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
