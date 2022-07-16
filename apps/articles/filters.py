from django_filters import rest_framework as django_filters

from .models import Article
from rest_framework import filters


class ArticleFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name="author", lookup_expr="username")
    class Meta:
        model = Article
        fields = ["author"]



class SearchBasedOnAuthorFilter(filters.SearchFilter):
    search_param = "author"