class ReadKeywordSerializer:
    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"][self.input_keyword]

        super(self.__class__, self).__init__(*args, **kwargs)