from rest_framework.renderers import JSONRenderer
from collections.abc import Sequence, Mapping


class ApplicationJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context["response"].status_code in [200, 201]:
            if isinstance(data, Sequence): # If the object is a list of objects.
                data = {
                    self.list_label: data
                }
            elif isinstance(data, Mapping): # If the returned value refers a single object.
                data = {
                    self.object_label: data
                }

        return super().render(data, accepted_media_type, renderer_context)