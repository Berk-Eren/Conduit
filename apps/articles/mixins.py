from datetime import datetime
from rest_framework import serializers


class TimeFieldSerializerMixin(serializers.ModelSerializer):
    output_format = "%Y-%m-%d %H:%M:%S"

    created = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField()

    def get_created(self, obj):
        return datetime.strftime(obj.created_at, self.output_format)

    def get_updated(self, obj):
        return datetime.strftime(obj.updated_at, self.output_format)
