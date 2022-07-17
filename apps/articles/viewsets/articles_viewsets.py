from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..serializers import ArticleSerializer
from ..models import Article, Tag, Comment
from ..filters import ArticleFilter, SearchBasedOnAuthorFilter
from ..renderers import ArticleJSONRenderer
from ..permissions import UserIsNotAuthorOfArticlePermission

from apps.core.shortcuts import get_object_or_404


class ArticleViewSet(viewsets.GenericViewSet):
    """
    For creating an article and getting a list of articles.
    """
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend]#[SearchBasedOnAuthorFilter]#[filters.SearchFilter]
    filterset_class = ArticleFilter
    serializer_class = ArticleSerializer
    renderer_classes = [ArticleJSONRenderer]
    permission_classes = [UserIsNotAuthorOfArticlePermission]
    lookup_field = "slug"
    filterset_fields = ['author__username']
    # search_fields = ["$author__username"]
    
    def list(self, request):
        """
        For getting a list of articles.
        """
        articles = self.filter_queryset(self.queryset)#Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """
        For creating an article.
        """
        serializer = ArticleSerializer(data=request.data, context={"author": request.user})

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def like(self, request, slug=None):
        article = self.get_object()

        if not article.liked_by.filter(id=request.user.id).exists():
            if article.disliked_by.filter(id=request.user.id).exists():
                article.disliked_by.remove(request.user.id)
                article.number_of_dislikes -= 1

            article.liked_by.add(request.user.id)
            article.number_of_likes += 1
            article.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response({
                "message": (
                    f"The article {article.title} was already liked "
                     "by user {request.user.username}!" )
            }, status=status.HTTP_204_NO_CONTENT)

    @like.mapping.delete
    def unset_like(self, request, slug=None):
        article = get_object_or_404(Article, slug=slug)
        
        if article.liked_by.filter(id=request.user.id).exists():
            article.liked_by.remove(request.user.id)
            article.number_of_likes -= 1
            article.save()

            return Response(status=status.HTTP_201_CREATED)
        
        return Response({
                "message": (
                    f"The user {request.user.username} didn't "
                    "like the article {article.title} yet."
                )
            }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def dislike(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        
        if not article.disliked_by.filter(id=request.user.id).exists():
            if article.liked_by.filter(id=request.user.id).exists():
                article.liked_by.remove(request.user.id)
                article.number_of_likes -= 1

            article.disliked_by.add(request.user.id)
            article.number_of_dislikes += 1
            article.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response({
                "message": (
                    f"The article {article.title} was already disliked "
                     "by user {request.user.username}!" )
            }, status=status.HTTP_204_NO_CONTENT)

    @dislike.mapping.delete
    def unset_dislike(self, request, slug=None):
        article = get_object_or_404(Article, slug=slug)
        
        if article.disliked_by.filter(id=request.user.id).exists():
            article.disliked_by.remove(request.user.id)
            article.number_of_dislikes -= 1
            article.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response({
                "message": (
                    f"The user {request.user.usernmae} didn't "
                    "dislike the article {article.title} yet."
                )
            }, status=status.HTTP_204_NO_CONTENT)


class ArticleUpdateDestroyView(DestroyAPIView, UpdateAPIView, RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "slug"
    renderer_classes = [ArticleJSONRenderer]