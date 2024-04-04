from django.contrib import admin
from .models import CustomUser, Task_todo

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Task_todo)