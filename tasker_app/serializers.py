from rest_framework import serializers
from .models import Task_todo

class Task_todoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_todo
        fields = ('id', 'title', 'description', 'status', 'owner')

