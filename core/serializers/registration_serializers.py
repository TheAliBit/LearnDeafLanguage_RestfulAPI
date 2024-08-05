from django.core.validators import EmailValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import re
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, required=True, label='شماره تلفن')
    password = serializers.CharField(write_only=True, required=True, label='رمز عبور')

    # first_name = serializers.CharField(write_only=True, label='نام')
    # last_name = serializers.CharField(write_only=True, label="نام خانوادگی")
    # email = serializers.EmailField(write_only=True, allow_blank=True, label="ایمیل")

    class Meta:
        model = User
        fields = [
            'phone_number', 'password',
            'first_name', 'last_name',
            'birth_date', 'email', 'avatar'
        ]

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

    # def validate_email(self, value):
    #     allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
    #     if value:
    #         domain = value.split('@')[1]
    #         if domain not in allowed_domains:
    #             raise serializers.ValidationError(
    #                 f'ایمیل باید یکی از این دامنه‌ها را داشته باشد: {", ".join(allowed_domains)}')
    #
    #     return value

    # def validate_last_name(self, value):
    #     first_name = self.initial_data.get('first_name')
    #     if value == first_name:
    #         raise serializers.ValidationError('نام خانوادگی نمی تواند با نام یکی باشد')
    #     return value

    # write and apply validaton for all data
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com']

        # if last_name == first_name:
        #     raise serializers.ValidationError('نام خانوادگی نمی تواند با نام یکی باشد')
        if email:
            domain = email.split('@')[1]
            if domain not in allowed_domains:
                raise serializers.ValidationError(
                    f'ایمیل باید یکی از این دامنه‌ها را داشته باشد: {", ".join(allowed_domains)}')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('phone_number')
        user = User.objects.create_user(username=username,
                                        password=password, **validated_data)
        return user
    # def create(self, validated_data):
    #     # Extract the password and remove it from validated_data
    #     password = validated_data.pop('password')
    #
    #     # Check if `phone_number` is used as the username
    #     if 'phone_number' in validated_data:
    #         username = validated_data.pop('phone_number')
    #     else:
    #         # Handle if `phone_number` is not present
    #         raise serializers.ValidationError("Phone number is required")
    #
    #     # Create the user with the appropriate fields
    #     user = User.objects.create_user(
    #         username=username,
    #         password=password,
    #         **validated_data
    #     )
    #
    #     return user


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
