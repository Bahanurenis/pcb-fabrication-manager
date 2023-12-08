from typing import List
import sys


class Config:
    def __init__(self, config_file: dict):
        self._config: dict = {}
        self._headers_list: List[Header] = []
        if self.validate(config_file):
            self._headers_list = self.set_headers_list(config_file["headers"])
            if self._headers_list != []:
                self._config = config_file

    def validate(self, config_file: dict):
        if "headers" not in config_file.keys():
            raise Exception(
                "config file should have 'headers' field, please check the documentation "
            )
            return False
        else:
            if config_file["headers"] == []:
                raise Exception(
                    "config file 'headers' shouldn't be empty, please check the documentation "
                )
            elif type(config_file["headers"]) != list:
                headers_value_type = type(config_file["headers"])
                raise Exception(
                    f" config file 'headers' should have list of parameters, but given config's header values type is {headers_value_type}, please check the documentation"
                )
                return False
            else:
                return True

    def set_headers_list(self, headers_list: list):
        _headers: List[Header] = []
        for item in headers_list:
            header = Header(item)
            if header == None:
                _headers.clear()
                break
            else:
                _headers.append(header)
        return _headers

    @property
    def headers(self):
        if self._headers_list != []:
            return self._headers_list


class Header:
    def __init__(self, item: dict):
        if self.validate(item):
            self._name = item["name"]
            if "required" in item.keys() and item["required"] != None:
                self._required = item["required"]
            else:
                self._required = False
            if (
                "mapping-name" not in item.keys()
                or item["mapping-name"] == None
                or item["mapping-name"] == ""
            ):
                self._mapping_name = self._name
            else:
                self._mapping_name = item["mapping-name"]

    def validate(self, item: dict):
        if (
            "name" not in item.keys()
            or item["name"] == None
            or item["name"] == ""
            or type(item["name"]) != str
        ):
            raise SyntaxError(
                " config file's headers' item should have 'name:' key and it should be string value "
            )
            return False
        else:
            if "required" in item.keys() and (
                item["required"] is not None
                and isinstance(item["required"], bool) == False
            ):
                raise TypeError(
                    " config file's headers' item's required field can have only bool  or None value"
                )
                return False
            if "mapping-name" in item.keys() and (
                type(item["mapping-name"]) != str and item["mapping-name"] != None
            ):
                raise TypeError(
                    "config file's headers' item's mapping-name field can have string or None value"
                )
                return False
            else:
                return True

    @property
    def name(self) -> str:
        return self._name

    @property
    def required(self):
        return self._required

    @property
    def mapping_name(self) -> str:
        return self._mapping_name
