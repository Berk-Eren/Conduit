from re import A
from rest_framework import serializers
from yaml import serialize

from .models import Article, Comment, Tag
from .mixins import TimeFieldSerializerMixin
from .relations import CommentStringRelatedField
from apps.core.decorators import KeywordNestedSerializer


#@KeywordNestedSerializer("tag", many="tags")
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        #fields = "__all__"
        exclude = [ "id", ]


# @KeywordNestedSerializer("article", many="articles")
class ArticleSerializer(TimeFieldSerializerMixin):
    comments = CommentStringRelatedField(many=True, source="main_comments", read_only=True)
    include_tags = serializers.ListSerializer(
        child=serializers.CharField(), write_only=True )
    tags = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Article
        # fields = ["comments", "tags", "created"]
        exclude = [ "id", "created_at", "updated_at"]
        #list_serializer_class = DictionarySerializer

    def create(self, validated_data):
        tags = validated_data.pop("include_tags", None)
        instance = super().create(validated_data)

        if type(tags) == list:
            for tag_title in tags:
                tag_ins = Tag.objects.get_or_create(title=tag_title)
                instance.tags.add(tag_ins[0].id)

        return instance

#@KeywordNestedSerializer("comment", many="comments")
class CommentSerializer(TimeFieldSerializerMixin):
    class Meta:
        model = Comment
        #fields = '__all__'
        exclude = [ "id", "created_at", "updated_at", "number_of_likes",
                    "is_deleted", "is_edited" ]
        read_only_fields = ["comments", ]

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)

        super().__init__(*args, **kwargs)

        if exclude is not None:
            if type(exclude) == str:
                exclude = [exclude]
            
            for field_name in exclude:
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        instance.is_edited = True
        return super().update(instance, validated_data)