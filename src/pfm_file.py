import sys
from pathlib import Path
from enum import Enum
import yaml
import pandas as pd


class FileTypeEnum(Enum):
    YAML = ("yaml",)
    CSV = ("csv",)
    UNKNOWN = ("UNKNOWN",)


class PfmFile:
    sys.tracebacklimit = 0

    def __init__(self, path: Path):
        self._path: Path = path
        self._file_type: FileTypeEnum = self._set_file_type(self._path)
        self._is_valid: bool = self._validate(self._path, self._file_type)

    def _set_file_type(self, path: Path):
        _type = FileTypeEnum
        if path.suffix in [".yaml", ".yml"]:
            return _type.YAML
        elif path.suffix == ".csv":
            return _type.CSV
        else:
            return _type.UNKNOWN

    def _validate(self, path: Path, file_type):
        if path.is_file() is not True:
            raise FileNotFoundError(f"{path} is not file")
            return False
        if file_type == FileTypeEnum.UNKNOWN:
            raise Exception(
                f" file is not recognized, please be ensure give the correct file type"
            )
            return False
        else:
            return True

    @property
    def file_path(self):
        if self._is_valid:
            return self._path

    @property
    def file_type(self):
        if self._is_valid:
            return self._file_type


class PfmYaml(PfmFile):
    def __init__(self, path: Path):
        super().__init__(path=path)


class PfmCsv(PfmFile):
    def __init__(self, path: Path):
        super().__init__(path=path)
