from pathlib import Path
import pandas as pd
from pfm_file import PfmCsv, FileTypeEnum


class PfmCsvHandler:
    def __init__(self, csv_file: PfmCsv):
        self._df: pd.DataFrame
        if csv_file.file_type != FileTypeEnum.CSV:
            raise TypeError(
                f" file extension should be '.csv', given file extension was {input_csv.file_type.value}"
            )
        with open(csv_file.file_path, "r") as file:
            self._df = pd.read_csv(file, on_bad_lines="warn")

    def get_columns(self):
        _columns: pd.Index = self._df.columns
        return _columns.values

    def update_csv_data(self, new_columns: dict) -> None:
        self._df.rename(columns=new_columns, inplace=True)

    def save_csv_data(self, output_csv_path: Path):
        self._df.to_csv(output_csv_path, encoding="utf-8", index=False)


if __name__ == "__main__":
    p = Path().cwd() / "input.csv"
    fi = PfmCsv(p)
    csv_handler = PfmCsvHandler(fi)
    a = csv_handler.get_columns()
    print(a)
