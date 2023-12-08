from pathlib import Path
import yaml
import pandas as pd


class PfmFile:
    def __init__(self):
        pass

    def is_file_valid(self, path: Path, suffixs: dict):
        if path.is_file() is not True:
            raise Exception(f"{path} is not file")
            return False
        elif path.suffix not in suffixs:
            raise Exception(f"config file's suffix should  be one of {suffixs}")
            return False
        else:
            return True


class PfmYaml(PfmFile):
    def __init__(self):
        super().__init__()
        self._yaml: dict = []

    @property
    def yaml(self) -> dict:
        return self._yaml

    @yaml.setter
    def yaml(self, value: Path):
        _p: Path = value
        if super().is_file_valid(_p, [".yaml", ".yml"]) is not True:
            self._yaml = None
        else:
            with open(_p, "r") as file:
                self._yaml = yaml.safe_load(file)


class PfmCsv(PfmFile):
    def __init__(self):
        super().__init__()
        self._csv: pd.DataFrame = None

    @property
    def csv(self) -> pd.DataFrame:
        return self._csv

    @csv.setter
    def csv(self, value):
        _p: Path = value
        if (
            super().is_file_valid(
                _p,
                [".csv"],
            )
            is not True
        ):
            self._csv = None
        else:
            with open(_p, "r") as file:
                self._csv = pd.read_csv(file, on_bad_lines="warn")
