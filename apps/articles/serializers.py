from re import A
from rest_framework import serializers
from yaml import serialize

from .models import Article, Comment, Tag
from .mixins import TimeFieldSerializerMixin
from .relations import CommentStringRelatedField
from apps.core.mixins import ReadKeywordData


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        #fields = "__all__"
        exclude = [ "id", ]


class ArticleSerializer(ReadKeywordData, TimeFieldSerializerMixin):
    comments = CommentStringRelatedField(many=True, source="main_comments", read_only=True)
    include_tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, default=["default_tag"], label="Article Tags" )
    tags = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    input_keyword = "article"
    
    class Meta:
        model = Article
        # fields = ["comments", "tags", "created"]
        exclude = [ "id", "created_at", "updated_at"]
        read_only_fields = ["number_of_shares", "number_of_likes", 
                             "number_of_dislikes", "liked_by", "disliked_by",
                              "slug" ]
        #list_serializer_class = DictionarySerializer

    def create(self, validated_data):
        validated_data["author"] = self.context["author"]
        tags = validated_data.pop("include_tags", None)

        instance = super().create(validated_data)

        if type(tags) == list:
            for tag_title in tags:
                tag_ins = Tag.objects.get_or_create(title=tag_title)
                instance.tags.add(tag_ins[0].id)

        return instance


class CommentSerializer(ReadKeywordData, TimeFieldSerializerMixin):
    class Meta:
        model = Comment
        #fields = '__all__'
        exclude = [ "id", "created_at", "updated_at", "number_of_likes",
                    "is_deleted", "is_edited" ]
        read_only_fields = ["comments", ]

    def update(self, instance, validated_data):
        instance.is_edited = True
        return super().update(instance, validated_data)