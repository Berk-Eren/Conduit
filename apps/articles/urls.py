from .viewsets.articles_viewsets import ArticleViewSet, ArticleUpdateDestroyView
from .viewsets.tags_viewsets import TagViewSet
from django.urls import path
from . import views
from rest_framework import routers


article_list = ArticleViewSet.as_view({'get': 'list', 'post': 'create'})

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)



urlpatterns = [
    # path('articles/',article_list, name="article-list"),
    path('articles/<str:slug>/', ArticleUpdateDestroyView.as_view(), name="article-destroy"),
    path('articles/<str:slug>/comments/', views.comment_on_article),
    path('articles/<str:slug>/comments/<int:instance_id>/', views.comment_on_article),
]
urlpatterns += router.urls