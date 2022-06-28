from re import A
from rest_framework import serializers

from .models import Article, Comment, Tag
from .mixins import TimeFieldSerializerMixin
from .relations import CommentStringRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        #fields = "__all__"
        exclude = [ "id", ]

    def validate(self, *args, **kwargs):
        return super().validate(*args, **kwargs)


class ArticleSerializer(TimeFieldSerializerMixin):
    comments = CommentStringRelatedField(many=True, source="main_comments", read_only=True)
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Article
        # fields = ["comments", "tags", "created"]
        exclude = [ "id", "created_at", "updated_at"]


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