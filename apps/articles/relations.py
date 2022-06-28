from rest_framework import serializers


class CommentStringRelatedField(serializers.StringRelatedField):
    content_threshold = 10

    def to_representation(self, obj):
        if not obj.is_subcomment_of.all().exists():
            content = obj.content[:self.content_threshold]
            post_text = "..." if len(obj.content)>self.content_threshold\
                               else ""

            return content + post_text
