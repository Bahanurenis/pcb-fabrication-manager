from pathlib import Path
import pandas as pd
from pfm_file import PfmCsv, FileTypeEnum
from config import Config


class PfmCsvHandler:
    def __init__(self, config: Config, dataFrame: pd.DataFrame):
        if dataFrame.empty:
            raise AttributeError(f"data is not correct")
        self._df: pd.DataFrame = dataFrame
        self._config: Config = config

    # For the PFM command line app
    @classmethod
    def from_PfmCsvFile(cls, config: Config, csv_file: PfmCsv):
        if csv_file.file_type != FileTypeEnum.CSV:
            raise TypeError(
                f" file extension should be '.csv', given file extension was {input_csv.file_type.value}"
            )
        with open(csv_file.file_path, "r") as file:
            _df: pd.DataFrame = pd.read_csv(file, on_bad_lines="warn")
            return cls(config=config, dataFrame=_df)

    def _update_columns(self):
        _csv_columns: pd.Index.values = self._df.columns.values
        _new_columns: dict = {}
        for header in self._config.headers:
            if header.name not in _csv_columns and header.required == True:
                raise Exception(
                    f"{header.name} is required ,but it couldn't find in the csv columns"
                )
                break
            else:
                _new_columns[header.name] = header.mapping_name
        self._df.rename(columns=_new_columns, inplace=True)

    def _update_rows(self):
        for row in self._config.rows:
            _to_replace = list(row.keys())[0]
            print(f"to_replace = {_to_replace}")
            _value = row.get(_to_replace)
            print(f"value = {_value}")
            self._df.replace(to_replace=_to_replace, value=_value, inplace=True)

    def export_new_csv_data(self, output_csv_path: Path):
        self._update_columns()
        self._update_rows()
        self._df.to_csv(output_csv_path, encoding="utf-8", index=False)
