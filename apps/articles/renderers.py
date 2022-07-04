from apps.core.renderers import ApplicationJSONRenderer


class ArticleJSONRenderer(ApplicationJSONRenderer):
    object_label = "article"
    list_label = "articles"


class TagJSONRenderer(ApplicationJSONRenderer):
    object_label = "tag"
    list_label = "tags"


class CommentJSONRenderer(ApplicationJSONRenderer):
    object_label = "comment"
    list_label = "comments"