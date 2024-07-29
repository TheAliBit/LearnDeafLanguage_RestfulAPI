# from rest_framework import serializers
# from .models import Profile
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id', 'username', 'first_name', 'last_name', 'age', 'birth_date', 'email', 'membership',
#                   'liked_words', 'avatar']
#         read_only_fields = ['id']
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     first_name = serializers.CharField(default="DefaultFirstName")
#     last_name = serializers.CharField(default="DefaultLastName")
#     age = serializers.IntegerField(default=18)
#     membership = serializers.BooleanField(default=False)
#
#     class Meta:
#         model = Profile
#         fields = ['username', 'password', 'email', 'first_name', 'last_name', 'age', 'membership']
#
#     def create(self, validated_data):
#         user = Profile.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data.get('email', ''),
#             first_name=validated_data.get('first_name', 'DefaultFirstName'),
#             last_name=validated_data.get('last_name', 'DefaultLastName'),
#             age=validated_data.get('age', 18),
#             membership=validated_data.get('membership', False),
#         )
#         return user


# from rest_framework import serializers
# from .models import Profile
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id', 'username', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance


# from rest_framework import serializers
# from .models import Profile

#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Profile
#         fields = ['id', 'username', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'id': {'read_only': True},
#         }
#
#
# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from rest_framework.validators import UniqueValidator
# from phonenumber_field.serializerfields import PhoneNumberField
# import re
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
#
# User = get_user_model()
#
#
# class SignupSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(unique=True, verbose_name='شماره تلفن')
#     password = serializers.CharField(max_length=128, verbose_name='رمز عبور')
#
#     class Meta:
#         model = User
#         fields = ['phone_number', 'password']
#
#     def validate_username(self, value):
#         phone_number_pattern = r'^09[0-9]{9}$'
#         if not re.match(phone_number_pattern, value):
#             raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
#         elif not User.objects.filter(username=value).exists():
#             raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود ندارد!')
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(username=validated_data['phone_number'], password=validated_data['password'])
#         return user
#
#
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(unique=True, verbose_name='شماره تلفن')
#     password = serializers.CharField(max_length=128, verbose_name='رمز عبور')
#
#     def validate_username(self, value):
#         phone_number_pattern = r'^09[0-9]{9}$'
#         if not re.match(phone_number_pattern, value):
#             raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
#         elif not User.objects.filter(username=value).exists():
#             raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود ندارد!')
#         return value
#
# def validate_password(self, value):
#     if len(value) < 8:
#         raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد!')
#     return value


#
#
# class RefreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField(max_length=2500, required=True, label='رفرش توکن')
#
#     def validate_refresh(self, value):
#         try:
#             RefreshToken(value)
#         except Exception as e:
#             raise serializers.ValidationError('توکن نامعتبر است!')
#         return value

# from rest_framework import serializers
# from django.contrib.auth import get_user_model, authenticate
# from django.core.validators import FileExtensionValidator
# import re
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
#
# User = get_user_model()
#
#
# class SignupSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(max_length=20, required=True, label='شماره تلفن')
#     password = serializers.CharField(write_only=True, required=True, label='رمز عبور')
#
#     class Meta:
#         model = User
#         fields = ['phone_number', 'password']
#
#     def validate_phone_number(self, value):
#         persian_phone_number_pattern = r'^09[0-9]{9}$'
#         if not re.match(persian_phone_number_pattern, value):
#             raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
#         elif User.objects.filter(username=value).exists():
#             raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود دارد!')
#         return value
#
#     def validate_password(self, value):
#         if len(value) < 8:
#             raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد!')
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(username=validated_data['phone_number'], password=validated_data['password'])
#         return user
#
#
# class LoginSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(max_length=20, required=True, label='شماره تلفن')
#     password = serializers.CharField(write_only=True, required=True, label='رمز عبور')
#
#     def validate_phone_number(self, value):
#         persian_phone_number_pattern = r'^09[0-9]{9}$'
#         if not re.match(persian_phone_number_pattern, value):
#             raise serializers.ValidationError('شماره تلفن وارد شده معتبر نمی باشد!')
#         elif not User.objects.filter(username=value).exists():
#             raise serializers.ValidationError('کاربری با شماره تلفن وارد شده وجود ندارد!')
#         return value
#
#     def validate_password(self, value):
#         if len(value) < 8:
#             raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد!')
#         return value
#
#     def validate(self, data):
#         user = authenticate(username=data['phone_number'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است!')
#         return data
#
#
# class RefreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField(max_length=2500, required=True, label='رفرش توکن')
#
#     def validate_refresh(self, value):
#         try:
#             RefreshToken(value)
#         except Exception as e:
#             raise serializers.ValidationError('توکن نامعتبر است!')
#         return value
