from rest_framework import serializers
from words.serializers.word_list_and_details import SimpleWordSerializer
from core.models import Profile
from words.models import Word


class ProfileSerializer(serializers.ModelSerializer):
    liked_words = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'last_name',
            'birth_date', 'email', 'membership', 'avatar', 'liked_words'
        ]

    def get_liked_words(self, obj):
        list = Word.objects.filter(liked_by=obj)
        return SimpleWordSerializer(list, many=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author']['url'] = reverse('author-detail', args=[instance.author.id], request=self.context.get('request'))
        ret['url'] = reverse('book-detail', args=[instance.id], request=self.context.get('request'))
        return ret
