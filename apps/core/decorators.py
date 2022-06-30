from rest_framework import serializers


def return_init_method(keyword):
    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"][keyword]
        
        super(self.__class__, self).__init__(*args, **kwargs) 
    return __init__

def return_model_serializer_data_method(keyword):
    def data(self):
        return {
            keyword: super(self.__class__, self).data
        }

    return property(data)

def return_list_serializer_class_data_method(keyword):
    class CustomListSerializer(serializers.ListSerializer):
        @property
        def data(self):
            return {
                keyword: super(self.__class__, self).data
            }

    return CustomListSerializer

class KeywordNestedSerializer:
    def __init__(self, keyword, many=None):
        self._keyword = keyword
        self._many_keyword = many

    def __call__(self, serializer_class):
        serializer_class.__init__ = return_init_method(self._keyword)

        if issubclass(serializer_class, serializers.ModelSerializer):
            serializer_class.data = return_model_serializer_data_method(
                                            self._keyword )

        if self._many_keyword:
            list_serializer_class = return_list_serializer_class_data_method(
                self._many_keyword )
            serializer_class.Meta.list_serializer_class = list_serializer_class
        
        return serializer_class
