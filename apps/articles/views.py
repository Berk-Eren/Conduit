from xml.etree.ElementTree import Comment
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

from apps.core.shortcuts import get_object_or_404
from .renderers import CommentJSONRenderer


@api_view(["GET", "POST", "DELETE", "PUT"])
@renderer_classes([CommentJSONRenderer])
def comment_on_article(request, slug, instance_id=None):
    if request.method == "GET":
        article = Article.objects.get(slug=slug)
        serializer = CommentSerializer(article.comment_set.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        article = Article.objects.get(slug=slug)
        is_subcomment_of = request.data.get("is_subcomment_of", None)
        
        serializer = CommentSerializer(data={**request.data,
                                                **{"articles": article}} )
        
        if serializer.is_valid():
            if is_subcomment_of:
                instance = get_object_or_404(Comment, article=article, id=is_subcomment_of)
                comment_instance = serializer.save()

                instance.comments.add(comment_instance)
            else:
                comment_instance = serializer.save()
            
            article.comment_set.add(comment_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        article = Article.objects.get(slug=slug)
        instance = get_object_or_404(Comment, article=article, id=instance_id)
        
        if instance.is_subcomment_of.filter(is_deleted=False).exists()\
                or instance.comments.filter(is_deleted=False).exists():
            instance.content = "This comment was deleted."
            instance.is_deleted = True
            
            instance.save()
        else:
            instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == "PUT":
        article = Article.objects.get(slug=slug)
        instance = get_object_or_404(Comment, article=article, id=instance_id)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
