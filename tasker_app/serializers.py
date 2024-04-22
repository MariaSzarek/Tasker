from rest_framework import serializers
from .models import Task_todo, CustomUser
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['id', 'name','last_name', 'password', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=16, min_length=6, write_only=True)

    default_error_messages = {
        'name_requirements': 'The name should only contain alphanumeric characters',
        'password_requirements' : 'Password must contain at least one digit and one special character'
    }

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('name', '')
        password = attrs.get('password', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages['name_requirements'])

        if not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError(self.default_error_messages['password_requirements'])

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)





class Task_todoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_todo
        fields = ('id', 'title', 'description', 'status', 'owner')

