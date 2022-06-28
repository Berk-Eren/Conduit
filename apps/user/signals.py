from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=models.User)
def create_token(sender, instance, *args, **kwargs):
    Token.objects.create(user=instance)


@receiver(post_save, sender=models.User)
def create_profile(sender, instance, *args, **kwargs):
    models.Profile.objects.create(user=instance)