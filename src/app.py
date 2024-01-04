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


# def map_yaml_to_csv(config: Config, csv_columns: pd.Index.values):
#     _new_columns: dict = {}
#     for header in config.headers:
#         if header.name not in csv_columns and header.required == True:
#             raise Exception(
#                 f"{header.name} is required ,but it couldn't find in the csv columns"
#             )
#             break
#         else:
#             _new_columns[header.name] = header.mapping_name
#     return _new_columns


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
    config_path: PfmYaml
    input_csv: PfmCsv
    if config == None:
        default_conf_path = Path.cwd() / "config.yaml"
        click.echo(
            click.style(
                f"W: Configuration wasn't passed, PFM will use the configuration yaml file from {default_conf_path}",
                fg="yellow",
            )
        )
        config_path = PfmYaml(default_conf_path)
    else:
        config_path = PfmYaml(config)

    input_csv = PfmCsv(inputfile)

    _config = PfmYamlParser(pfm_yaml=config_path).config
    _csv_handler = PfmCsvHandler.from_PfmCsvFile(config=_config, csv_file=input_csv)
    if outputfile.parent.exists() == False:
        click.echo(
            click.style(
                f"W: {outputfile.parent} is not exist, will be created",
                fg="yellow",
            )
        )
        outputfile.parent.mkdir(parents=True, exist_ok=True)

    click.echo(click.style("Progress...", fg="green"))
    _csv_handler.export_new_csv_data(output_csv_path=outputfile)
    click.echo(click.style("new csv file has been saved...", fg="green"))


if __name__ == "__main__":
    main()
