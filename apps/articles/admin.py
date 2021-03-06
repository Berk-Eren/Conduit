from django.contrib import admin
from .models import Article, Tag, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass