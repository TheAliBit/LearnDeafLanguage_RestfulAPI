from rest_framework.exceptions import ValidationError

from LDL import settings
from words.models import Word
from rest_framework import serializers


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'explanation', 'image', 'category']

    def validate(self, attrs):
        title = attrs.get('title')
        if title:
            if Word.objects.filter(title=title).exists():
                raise ValidationError({'message': '!کلمه تکراری است'})
        return attrs

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + \
                          instance.image.url if instance.image else None
        return result


class PremiumWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'title', 'explanation', 'image', 'video', 'category']

    def validate(self, attrs):
        title = attrs.get('title')
        if title:
            if Word.objects.filter(title=title).exists():
                raise ValidationError({'message': '!کلمه تکراری است'})
        return attrs

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + \
                          instance.image.url if instance.image else None
        result['video'] = settings.DOMAIN + \
                          instance.video.url if instance.video else None
        return result


# use an empty serializer to avoid using other serializer in the post method
class EmptySerializer(serializers.Serializer):
    ...


# simple word serializer to show id and title
class SimpleWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'title', 'image'
        ]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + \
                          instance.image.url if instance.image else None
        return result


class SimpleWordSerializerWithVideo(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'title', 'image', 'video'
        ]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['image'] = settings.DOMAIN + instance.image.url if instance.image else None
        result['video'] = settings.DOMAIN + instance.video.url if instance.video else None
        return result


# simple word serializer to show video
class VSimpleWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'video']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['video'] = settings.DOMAIN + instance.video.url if instance.video else None
        return result
