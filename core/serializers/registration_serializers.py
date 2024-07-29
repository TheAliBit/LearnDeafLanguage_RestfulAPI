from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import re
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class  SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, required=True, label='شماره تلفن')
    password = serializers.CharField(write_only=True, required=True, label='رمز عبور')

    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def validate_phone_number(self, value):
        persian_phone_number_pattern = r'^09[0-9]{9}$'
        if not re.match(persian_phone_number_pattern, value):
            raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود دارد!')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد!')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['phone_number'], password=validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, required=True, label='شماره تلفن')
    password = serializers.CharField(write_only=True, required=True, label='رمز عبور')

    def validate_phone_number(self, value):
        persian_phone_number_pattern = r'^09[0-9]{9}$'
        if not re.match(persian_phone_number_pattern, value):
            raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
        elif not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود ندارد!')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد!')
        return value

    def validate(self, data):
        user = authenticate(username=data['phone_number'], password=data['password'])
        if not user:
            raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است!')
        return data


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=2500, required=True, label='رفرش توکن')

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception as e:
            raise serializers.ValidationError('توکن نامعتبر است!')
        return value
