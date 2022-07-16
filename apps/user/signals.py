import os

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.files.storage import default_storage

from rest_framework.authtoken.models import Token

from . import models
from django.core.files.storage import FileSystemStorage

@receiver(post_save, sender=models.CustomUser)
def create_token(sender, instance, *args, **kwargs):
    Token.objects.get_or_create(user=instance)

@receiver(post_delete, sender=models.Profile)
def delete_profile_image_from_media(sender, instance, *args, **kwargs):
    top_directory = instance.image.name.split("/")[0]
    
    default_storage.delete(instance.image.name)
    default_storage.delete(top_directory)
