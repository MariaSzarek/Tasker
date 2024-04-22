from rest_framework import generics
from .serializers import Task_todoSerializer
from .models import Task_todo, CustomUser
from rest_framework import authentication, permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        current_site = get_current_site(request).domain
        relativeLink = reverse('activation-confirmed')
        absurl = 'http://' + current_site + relativeLink + "?token="+token.key
        email_body = "Witaj " + user.name.capitalize() + ",\nDziękujemy za rejestrację w Taskerze!\nKliknij w poniższy link, aby potwierdzić swój adres e-mail i dokończyć proces rejestracji:\n" + absurl + "\nJeśli nie rejestrowałeś/-aś się w Taskerze, prosimy o zignorowanie tej wiadomości.\nDziękujemy,\nZespół Tasker"
        data = {'to_email':user.email, 'email_body':email_body, 'email_subject': 'Witaj w Taskerze'}
        Util.send_email(data)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = UserSerializer
    def get(self, request):
        token = request.GET.get('token')
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
            serializer = UserSerializer(user)
            return Response({'token': token_obj.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

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

#http://127.0.0.1:8000/tasker/4/
class Task_todoItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task_todo.objects.all()
    serializer_class = Task_todoSerializer
