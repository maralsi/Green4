from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError



class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

class UserAuthSerializer(UserValidateSerializer):
    pass


class UserCreateSerializer(UserValidateSerializer):

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists!')
        return username

