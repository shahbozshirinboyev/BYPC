from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender="auth.User")
def ensure_profile(sender, instance, created, **kwargs):
    role = "admin" if instance.is_superuser else "guest"
    Profile.objects.get_or_create(user=instance, defaults={"role": role})
