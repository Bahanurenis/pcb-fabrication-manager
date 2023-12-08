import sys
from typing import List
from pathlib import Path
import click
import pandas as pd
import yaml

from yaml_parser import PfmYamlParser
from csv_handler import PfmCsvHandler
from pfm_file import PfmYaml, PfmCsv
from config import Config


def map_yaml_to_csv(y_p: Path, i_p: Path, o_p: Path):
    yaml_f = PfmYaml()
    yaml_f.yaml = y_p
    _configs: List[Config] = PfmYamlParser(yaml_f.yaml).parse_yaml()
    csv_f = PfmCsv()
    csv_f.csv = i_p
    _data_frame: pd.DataFrame = csv_f.csv
    csv_handler: PfmCsvHandler = PfmCsvHandler(data_frame=_data_frame)
    _columns: pd.Index = csv_handler.get_csv_columns()
    _new_columns: dict = {}
    for config in _configs:
        if config.column_name in _columns.values:
            if config.mapping_name != "" and config.column_name != config.mapping_name:
                _new_columns[config.column_name] = config.mapping_name
            else:
                pass
                # _new_columns[config["name"]] = config["name"]
        else:
            if config.required:
                raise Exception(
                    f"{config.column_name} is required but couldn't found in columns of .csv"
                )
                return
            else:
                # do nothing
                pass

    csv_handler.update_csv_columns(new_columns=_new_columns)
    if o_p.parent.exists():
        csv_handler.export_updated_csv(o_p)
    else:
        o_p.parent.mkdir(parents=True, exist_ok=True)
        csv_handler.export_updated_csv(o_p)


# TODO: we will use this logic later
def get_default_config():
    home = Path().home()
    if sys.platform == "win32":
        d_config = home / "AppData/Roaming/pfm/.config/config.yaml"
    elif sys.platform.startswith("linux"):
        d_config = home / ".local/share/pfm/.config/config.yaml"
    try:
        d_config.mkdir(parents=True)
    except FileExistsError:
        pass


@click.command()
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=False,
        path_type=Path,
    ),
    required=False,
    show_default=True,
)
@click.argument(
    "inputfile",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        resolve_path=False,
        path_type=Path,
        executable=False,
    ),
)
@click.argument(
    "outputfile",
    required=True,
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        resolve_path=False,
        path_type=Path,
        executable=False,
    ),
)
def main(config: Path, inputfile: Path, outputfile: Path):
    config_path: Path
    if config == None:
        config_path: Path = Path.cwd() / "config.yaml"
    else:
        config_path: Path = config
    map_yaml_to_csv(y_p=config_path, i_p=inputfile, o_p=outputfile)


if __name__ == "__main__":
    main()
