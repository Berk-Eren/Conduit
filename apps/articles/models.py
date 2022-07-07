from django.db import models

from apps.core.models import BaseTimeModel
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.core.validators import validate_slug

from apps.user.models import User


class Article(BaseTimeModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, null=True)
    content = models.TextField(validators=[MinLengthValidator(50)], blank=True)
    number_of_likes = models.IntegerField(default=0)
    number_of_dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_articles", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="disliked_articles", blank=True)
    number_of_shares = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tag", blank=True)
    slug = models.SlugField(db_index=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def main_comments(self):
        return self.comment_set.filter(is_subcomment_of__isnull=True)


class Tag(models.Model):
    title = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.title + " - " + str(self.id)


class Comment(BaseTimeModel):
    content = models.TextField()
    number_of_likes = models.IntegerField(default=0)
    comments = models.ManyToManyField("self", related_name="is_subcomment_of",
                                        symmetrical=False, blank=True)
    articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        pre_text = "The article '%s' was commented" % (self.articles.title)

        if self.commented_by:
            pre_text += " by '%s'" % (self.commented_by.username)

        return pre_text + " - %d" % self.id