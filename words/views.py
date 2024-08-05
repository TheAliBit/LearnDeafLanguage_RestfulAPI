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
    VSimpleWordSerializer, PremiumWordSerializer


# TODO: add permissions for views
# TODO: add pagination : DONE
# TODO: move filter backends to settings.py : DONE

class CategoryViewSet(ModelViewSet):
    # TODO: return parent none categories when no filter applied
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    filterset_fields = ['parent']


class WordViewSet(ModelViewSet):
    # TODO: remove video field for false membership users
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

    # liking and unliking the word
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


# TODO: add video exam for membership true users
# writing the exam APIView
class ExamViewSet(ViewSet):
    def list(self, request):
        # ordering objects in a random order and slice the first 4
        # don't user order_by '?' it's a very bad query
        # words = Word.objects.order_by('?')[:4] -> -X-
        word_ids = Word.objects.values_list('id', flat=True)
        # Randomly select 4 unique primary keys
        random_ids = random.sample(list(word_ids), 4)
        random_words = Word.objects.filter(id__in=random_ids)
        # serializing the word instances
        serializer = SimpleWordSerializer(random_words, many=True)

        response_data = {
            "exam": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


# Here i want to add the sentence building section
class SentenceMakerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        word_ids = request.data.get('ids')
        if not word_ids or not isinstance(word_ids, list):
            return Response({'error': 'A list of IDs is required'}, status=status.HTTP_400_BAD_REQUEST)
        words = Word.objects.filter(id__in=word_ids)
        serializer = VSimpleWordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
