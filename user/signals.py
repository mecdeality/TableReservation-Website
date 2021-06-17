from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import AccountType


@receiver(post_save, sender=User)
def create_status(sender, instance, created, **kwargs):
    if created:
        st = AccountType.objects.create(user=instance)
        st.save()

