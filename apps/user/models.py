import os

from django.db import models
from django.contrib.auth.models import AbstractUser as auth_models_User


def profile_image_upload_to(instance, filename):
    extendsion = os.path.splitext(filename)[-1]
    return "{0}/profile{1}".format(instance.user.username, extendsion)


class CustomUser(auth_models_User):

    def __str__(self):
        return self.username + " : " + str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    image = models.ImageField(upload_to=profile_image_upload_to, blank=True)
    biography = models.TextField(blank=True)
    following = models.ManyToManyField("self", related_name="followed_by", 
                                        symmetrical = False, blank=True)
