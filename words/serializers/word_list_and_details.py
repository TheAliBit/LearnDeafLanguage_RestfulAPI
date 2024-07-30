from rest_framework import serializers
from words.models import Word, Category
from words.serializers.category_serializers import CategorySerializer


class WordSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'title', 'explanation', 'image', 'video', 'category_id', 'category_title']


# use a empty serializer to avoid using other serializer in the post method
class EmptySerializer(serializers.Serializer):
    ...
