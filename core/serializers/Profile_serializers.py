from rest_framework import serializers
from core.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'username', 'password', 'first_name', 'last_name',
            'age', 'birth_date', 'email', 'membership', 'liked_words', 'avatar'
        ]
