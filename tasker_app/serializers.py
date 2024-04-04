from rest_framework import serializers
from .models import Task_todo, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['id', 'name', 'password', 'email']

class Task_todoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_todo
        fields = ('id', 'title', 'description', 'status', 'owner')

