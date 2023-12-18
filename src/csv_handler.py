from pathlib import Path
import pandas as pd
from pfm_file import PfmCsv, FileTypeEnum
from config import Config


class PfmCsvHandler:
    def __init__(self, csv_file: PfmCsv, config: Config):
        self._df: pd.DataFrame
        self._config = config
        if csv_file.file_type != FileTypeEnum.CSV:
            raise TypeError(
                f" file extension should be '.csv', given file extension was {input_csv.file_type.value}"
            )
        with open(csv_file.file_path, "r") as file:
            self._df = pd.read_csv(file, on_bad_lines="warn")

    #  print(self._df)

    def _get_columns(self):
        return self._df.columns.values

    def _update_columns(self):
        _csv_columns: pd.Index.values = self._get_columns()
        _new_columns: dict = {}
        for header in self._config.headers:
            if header.name not in _csv_columns and header.required == True:
                raise Exception(
                    f"{header.name} is required ,but it couldn't find in the csv columns"
                )
                break
            else:
                _new_columns[header.name] = header.mapping_name
        self._df.rename(columns=new_columns, inplace=True)

    def _replace_row_values(self):
        pass

    def save_csv_data(self, output_csv_path: Path):
        self._df.to_csv(output_csv_path, encoding="utf-8", index=False)


if __name__ == "__main__":
    p = Path().cwd() / "input.csv"
    fi = PfmCsv(p)
    csv_handler = PfmCsvHandler(fi)
    a = csv_handler.get_columns()
    print(a)
