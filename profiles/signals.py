from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile if a new user was created
        Profile.objects.create(user=instance)
    else:
        # Existing user saved — just save the profile to update any changes
        instance.profile.save()