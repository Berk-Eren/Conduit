from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView

from ..serializers import ArticleSerializer
from ..models import Article, Tag, Comment


class ArticleViewSet(viewsets.ViewSet):
    
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data, context={"author": request.user})

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateDestroyView(DestroyAPIView, UpdateAPIView, RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "slug"