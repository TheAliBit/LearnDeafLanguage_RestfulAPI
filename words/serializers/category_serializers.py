from rest_framework import serializers

from LDL import settings
from words.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'parent', 'children']

    # def get_children(self, obj):
    #     children = Category.objects.filter(parent=obj)
    #     return CategorySerializer(children, many=True).data
    def get_children(self, obj):
        # Use values_list to get only the ids of the children
        children_ids = Category.objects.filter(parent=obj).values_list('id', flat=True)
        return children_ids
