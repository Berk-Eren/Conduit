from django.db import models

from apps.core.models import BaseTimeModel
from django.contrib.auth.models import User
from django.conf import settings


class Profile(BaseTimeModel):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False)
    image = models.ImageField(upload_to="static/images/", blank=True)
    archive = models.ManyToManyField("articles.Article", blank=True)

    def __str__(self):
        return self.user.username