import csv
import datetime as dt
from pathlib import Path
from typing import Iterable

from pep_parse.settings import DATETIME_FORMAT


def write_to_csv_file(file_path: Path, data: Iterable) -> None:
    """Write data to a csv file."""
    with open(file_path, mode='w', encoding='utf-8') as file:
        writer = csv.writer(
            file,
            dialect='unix',
            delimiter=';',
            quoting=csv.QUOTE_MINIMAL,
        )

        for row in data:
            writer.writerow(row)


def make_dir(base_dir: Path, dir_name: str) -> Path:
    """Create a new directory at the given base_dir path with the dir_name."""
    dir = base_dir / dir_name
    dir.mkdir(exist_ok=True)
    return dir


def cvs_file_name(prefix: str, date_format: str) -> str:

    now = dt.datetime.now()
    now_formatted = now.strftime(date_format)

    file_name = f'{prefix}_{now_formatted}.csv'
    return file_name


def csv_file_output(
        base_dir: Path,
        dir_name: str,
        file_prefix: str,
        data: Iterable
) -> None:
    date_format = DATETIME_FORMAT
    results_dir = make_dir(base_dir, dir_name)

    file_name = cvs_file_name(file_prefix, date_format)
    file_path = results_dir / file_name

    write_to_csv_file(file_path, data)
