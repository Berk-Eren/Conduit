class KeywordNestedSerializer:
    @staticmethod
    def return_init_method(keyword):
        def __init__(self, *args, **kwargs):
            if "data" in kwargs:
                kwargs["data"] = kwargs["data"][keyword]
            super(self.__class__, self).__init__(*args, **kwargs) 
        return __init__

    def __init__(self, keyword):
        self._keyword = keyword

    def __call__(self, serializer_class, *args, **kwargs):
        serializer_class.__init__ = KeywordNestedSerializer.return_init_method(self._keyword)
        return serializer_class
