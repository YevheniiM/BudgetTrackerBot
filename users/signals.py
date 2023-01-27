from django.db.models.signals import post_save
from django.dispatch import receiver

from budget.models import UserStatus, UserStatusEnum
from .models import User

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus.objects.create(user=instance, status=UserStatusEnum.DEFAULT)