
class ReadKeywordData:
    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            if self.input_keyword in kwargs["data"]:
                kwargs["data"] = kwargs["data"][self.input_keyword]

        super(ReadKeywordData, self).__init__(*args, **kwargs)