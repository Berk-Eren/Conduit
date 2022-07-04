from django.db import models
from django.contrib.auth.models import User as auth_models_User


class User(auth_models_User):
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username + " : " + str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    image = models.ImageField(blank=True)
    biography = models.TextField(blank=True)
    following = models.ManyToManyField("self", related_name="followed_by", 
                                        symmetrical = False, blank=True)
