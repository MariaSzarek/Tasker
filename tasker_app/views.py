from django.shortcuts import render
from rest_framework import viewsets
from .serializers import Task_todoSerializer
from .models import Task_todo

class Task_todoView(viewsets.ModelViewSet):
    queryset = Task_todo.objects.all()
    serializer_class = Task_todoSerializer
