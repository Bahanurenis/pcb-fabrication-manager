from pathlib import Path
from pfm_file import FileTypeEnum, PfmYaml
from config import Config
import yaml


class PfmYamlParser:
    def __init__(self, pfm_yaml: PfmYaml):
        self._config: Config = self._parse_yaml_file(pfm_yaml=pfm_yaml)

    def _parse_yaml_file(self, pfm_yaml: PfmYaml):
        _config: Config = None
        if pfm_yaml.file_type != FileTypeEnum.YAML:
            raise TypeError(
                f"PfmYamlParse can only take a .yaml file as an argument, given file extension was {pfm_yaml.file_type.value}"
            )
        else:
            with open(pfm_yaml.file_path, "r") as file:
                _config: Config = Config(yaml.safe_load(file))
        return _config

    @property
    def config(self):
        if self._config != None:
            return self._config
