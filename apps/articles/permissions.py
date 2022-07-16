from rest_framework import permissions


class UserIsNotAuthorOfArticlePermission(permissions.BasePermission):
    """
    Permissions for like/dislike actions on the article. User shouldn't be the author of the article.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user != obj.author