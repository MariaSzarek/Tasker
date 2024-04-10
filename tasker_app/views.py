from django.shortcuts import render
from rest_framework import  generics
from .serializers import Task_todoSerializer
from .models import Task_todo
from rest_framework import authentication, permissions


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response("Logged out successfully")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")





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
