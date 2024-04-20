from django.db import models
from .menagers import UserManager
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Task_todo(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('ABANDONED', 'Abandoned'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner_tasks', default='')

    #area =
    #category =
    #priority =
    #ddl =

    def __str__(self):
        return f"{self.title} -{self.status}"