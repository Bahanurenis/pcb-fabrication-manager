class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._column_name: str = ""
        self._required: bool = False
        self._mapping_name: str = ""
        if "name" in entries.keys():
            self._column_name: str = entries["name"]
        if "required" in entries.keys():
            self._required = entries["required"]
        if "mapping-name" in entries.keys() and entries["mapping-name"] is not None:
            self._mapping_name: str = entries["mapping-name"]

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def required(self):
        return self._required

    @property
    def mapping_name(self) -> str:
        return self._mapping_name

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
