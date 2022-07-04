from rest_framework.renderers import JSONRenderer
from collections.abc import Sequence, Mapping


class ApplicationJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, Sequence):
            data = {
                self.list_label: data
            }
        elif isinstance(data, Mapping):
            data = {
                self.object_label: data
            }

        return super().render(data, accepted_media_type, renderer_context)