from rest_framework import generics
from .serializers import Task_todoSerializer
from .models import Task_todo, CustomUser
from rest_framework import authentication, permissions

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import UserSerializer, RegisterSerializer
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import secrets
import string
from django.core.cache import cache
from django.utils import timezone

def generate_random_token(length=32):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(length))
    return token



@api_view(['POST'])
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        # token = RefreshToken.for_user(user)
        token = generate_random_token()

        cache.set(f'verification_token_{token}', user.id, timeout=300)
        current_site = get_current_site(request).domain
        relativeLink = reverse('activation-confirmed')
        # absurl = 'http://' + current_site + relativeLink + "?token="+str(token.access_token)
        absurl = 'http://' + current_site + relativeLink + "?token=" + token
        email_body = "Witaj " + user.name.capitalize() + ",\nDziękujemy za rejestrację w Taskerze!\nKliknij w poniższy link, aby potwierdzić swój adres e-mail i dokończyć proces rejestracji:\n" + absurl + "\nJeśli nie rejestrowałeś/-aś się w Taskerze, prosimy o zignorowanie tej wiadomości.\nDziękujemy,\nZespół Tasker"
        data = {'to_email':user.email, 'email_body':email_body, 'email_subject': 'Witaj w Taskerze'}
        Util.send_email(data)
        # return Response({'token': str(token.access_token), 'user': serializer.data})
        return Response({'token': token, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        token = request.GET.get('token')
        cache_token = cache.get(f'verification_token_{token}')

        if cache_token is not None:
            if isinstance(cache_token, dict):
                user_id = cache_token.get('user_id')
            else:
                user_id = cache_token

            if isinstance(user_id, int):
                user = CustomUser.objects.get(id=user_id)

                if user and not user.is_verified:
                    if token == cache_token:
                        user.is_verified = True
                        user.save()
                        serializer = UserSerializer(user)
                        cache.delete(f'verification_token_{token}')
                    # return Response({'token': cache_token, 'user': serializer.data}, status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = get_object_or_404(CustomUser, email=email)
    if not user.check_password(password):
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
    user.last_active = timezone.now()
    user.save()
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    serializer = UserSerializer(user)
    return Response({
        'access_token': str(access_token),
        'refresh_token': str(refresh_token),
#        'user': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        user_id = token.payload.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        user.last_active = timezone.now()
        user.save()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
    except KeyError:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)


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
