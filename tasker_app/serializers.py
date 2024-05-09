from rest_framework import serializers
from .models import Task_todo, CustomUser
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['id', 'name','last_name', 'password', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        'name_requirements': 'The name should only contain alphanumeric characters',
        'password_req_char' : 'Password must contain at least one digit and one special character',
        'password_req_length': 'Password must have a minimum of 6 characters and a maximum of 16'
    }


    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        last_name = attrs.get('last_name', '')
        password = attrs.get('password', '')

        if not name.isalpha() and not last_name.isalpha():
            raise serializers.ValidationError(
                self.default_error_messages['name_requirements'])

        if not re.search(r'\d', password) or not re.search(r'[!@#$%^&*_+=|/?~`\'".,<>()\[\]\{\}:;]', password):
            raise serializers.ValidationError(self.default_error_messages['password_req_char'])

        if len(password) > 16 or len(password) < 6:
            raise serializers.ValidationError(self.default_error_messages['password_req_length'])

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class Task_todoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_todo
        fields = ['title', 'description', 'owner', 'area', 'subcategory']
