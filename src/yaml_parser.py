from pathlib import Path
from pfm_file import PfmYaml
from typing import List
from config import Config


class PfmYamlParser:
    def __init__(self, yaml: dict):
        self._yaml: dict = yaml
        self._config_list: List[Config] = []

    def parse_yaml(self) -> List[Config]:
        _items: List[dict] = self._yaml["headers"]
        for item in _items:
            _config = Config(**item)
            self._config_list.append(_config)
        return self._config_list
