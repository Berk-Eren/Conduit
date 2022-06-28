from django.db import models

from apps.core.models import BaseTimeModel
from django.contrib.auth.models import User


class Profile(BaseTimeModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False)
    image = models.ImageField(upload_to="static/images/", blank=True)
    archive = models.ManyToManyField("articles.Article", blank=True)

    def __ste__(self):
        return self.user.username