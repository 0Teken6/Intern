from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class ArticleSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'time_created', 'time_updated', 'is_private', 'author_email']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'role']

    def validate_password(self, value):
            validate_password(value)
            return value


    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'follower')
        )
        return user