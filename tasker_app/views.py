from django.shortcuts import render
from rest_framework import  generics
from .serializers import Task_todoSerializer
from .models import Task_todo


from rest_framework import authentication, permissions
class Task_todoListView(generics.ListCreateAPIView):
    serializer_class = Task_todoSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
        ]

    permission_classes = [permissions.IsAuthenticated]

    #http://127.0.0.1:8000/tasker/?owner=3
    def get_queryset(self):
        queryset = Task_todo.objects.all()
        owner = self.request.query_params.get('owner')
        if owner is not None:
            queryset = queryset.filter(owner=owner)
        return queryset

class Task_todoItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task_todo.objects.all()
    serializer_class = Task_todoSerializer
