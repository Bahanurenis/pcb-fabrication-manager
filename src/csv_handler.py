from typing import List
from pathlib import Path
import pandas as pd
from pfm_file import PfmCsv


class PfmCsvHandler:
    def __init__(self, data_frame: pd.DataFrame):
        self._df: pd.DataFrame = data_frame

    def get_csv_columns(self) -> pd.Index:
        _columns: pd.Index = self._df.columns
        return _columns

    def update_csv_columns(self, new_columns: dict) -> None:
        self._df.rename(columns=new_columns, inplace=True)

    def export_updated_csv(self, o_p: Path) -> None:
        self._df.to_csv(o_p, encoding="utf-8", index=False)
