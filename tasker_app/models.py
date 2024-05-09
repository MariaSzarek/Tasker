from django.db import models
from .menagers import UserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=16, unique=True)
    password = models.CharField(max_length=255)
    username = None
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class VerifyEmailToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class Task_todo(models.Model):

   AREA_CHOICES = [
       (1, 'Mieszkanie'),
       (2, 'Ogród'),
   ]

   SUBCATEGORY = [
       (1, 'Sypialnia'),
       (2, 'Łazienka'),
   ]

   title = models.CharField(max_length=50)
   description = models.CharField(max_length=250)
   owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner_tasks', default='')
   area = models.PositiveSmallIntegerField(choices=AREA_CHOICES, default=1, null=True, blank=True)
   subcategory = models.PositiveSmallIntegerField(choices=SUBCATEGORY, default=1, null=True, blank=True)

   def __str__(self):
       return f"{self.id} {self.title} -{self.owner}"
