from rest_framework import serializers
from LDL import settings
from words.models import Category


class CategorySerializer(serializers.ModelSerializer):
    # DONE: if category is parent null,  must have picture

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'parent', 'children']

    # Custom validation
    def validate(self, data):
        parent = data.get('parent')
        image = data.get('image')
        title = data.get('title')
        if parent is None and not image:
            raise serializers.ValidationError({'message': '!دسته بندی های اصلی نمیتوانند بدون عکس باشند'})
        elif Category.objects.filter(title=title).exists():
            raise serializers.ValidationError({'message': '!کتگوری تکراری است'})
        return data

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        return result
