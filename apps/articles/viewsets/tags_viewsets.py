from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Tag
from ..serializers import TagSerializer
from ..renderers import TagJSONRenderer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    renderer_classes = [TagJSONRenderer]