from celery import shared_task
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta
@shared_task
def user_activity_checker():
    time_period = timezone.now() - timedelta(days=7)
    never_logged_in_users = CustomUser.objects.filter(
        last_active__isnull=True,
        created_at__lt=time_period
    )
    deleted_users = never_logged_in_users.delete()

    return f"Deleted {deleted_users[0]} users who never logged in and were registered more than 7 days ago."

result = user_activity_checker.delay()
print(result.status)
print(result.result)