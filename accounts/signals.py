from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, **kwargs):
    """
    Creates a profile for user instance when it's created
    """
    if kwargs.get("created"):
        Profile.objects.create(user=instance).save()
