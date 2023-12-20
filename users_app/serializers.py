from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users_app.models import CustomUser



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=15)
    password_confirm = serializers.CharField(write_only=True, min_length=8, max_length=15)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm'
        ]

    def validate(self, data):
        errors = {}
        validate_password(data['password'])
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают')
        if not any(char.isdigit() for char in data['password']):
            errors['password'] = errors.get('password', []) + ['Пароль должен содержать хотя бы одну цифру.']
        if not any(char.isupper() for char in data['password']):
            errors['password'] = errors.get('password', []) + ['Пароль должен содержать хотя бы одну заглавную букву.']
        if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in data['password']):
            errors['password'] = errors.get('password', []) + [
                'Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*(),.?":{}|<>).']

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        return CustomUser.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.pop('username', None)
        password = data.pop('password', None)

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                data['user'] = user
            else:
                raise serializers.ValidationError("Пользователь с таким логином и паролем не найден.")
        else:
            raise serializers.ValidationError("Необходимо указать логин и пароль.")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)


    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "avatar", "birth_date", "phone_number"]


class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["phone_number"]