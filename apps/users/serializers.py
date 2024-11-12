from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.db import transaction


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email"]


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=120,
        min_length=8,
        write_only=True,
        help_text="must not be less than 8",
        style={"input_type": "password"},
        required=True,
    )
    confirm_password = serializers.CharField(
        max_length=120,
        min_length=8,
        write_only=True,
        help_text="must match password",
        style={"input_type": "password"},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.pop("password")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email already exist in our database.")
        validated_data.pop("confirm_password")
        user: CustomUser = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError("Passwords do not match.")
        return attrs

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(key, value, instance)
        instance.save()
        return instance


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = CustomUser.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    """
    Generates refresh token for users and returns new access token
    """

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user = BasicUserSerializer(self.user)
        data["user"] = user.data
        return data