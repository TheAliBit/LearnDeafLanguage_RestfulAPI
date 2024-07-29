from rest_framework import serializers
from words.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'parent', 'children']

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        return CategorySerializer(children, many=True).data
