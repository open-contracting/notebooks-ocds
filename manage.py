#!/usr/bin/env python
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import click

directory = Path(__file__).resolve().parent


def yield_notebooks():
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if not filename.endswith('.ipynb'):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            notebook = json.load(f)

        yield filename, filepath, notebook


def yield_cells(notebook):
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            if '%%sql' not in source[0]:
                continue

            sql = ''.join(source[1:])
            pg_format = subprocess.run(['pg_format', '-f', '1'], input=sql, check=True, stdout=subprocess.PIPE,
                                       universal_newlines=True)

            yield source, cell, sql, pg_format.stdout


@click.group()
def cli():
    pass


@cli.command()
def pre_commit():
    """
    Format SQL cells in Jupyter Notebooks using pg_format.
    """
    for filename, filepath, notebook in yield_notebooks():
        for source, cell, sql, sql_formatted in yield_cells(notebook):
            cell['source'] = [source[0], "\n"] + sql_formatted.splitlines(keepends=True)

        with open(filepath, 'w') as f:
            json.dump(notebook, f, ensure_ascii=False, indent=2)
            f.write('\n')


@cli.command()
def check():
    """
    Check that SQL cells are formatted using pg_format.
    """
    warnings = False

    for filename, filepath, notebook in yield_notebooks():
        for source, cell, sql, sql_formatted in yield_cells(notebook):
            if sql.strip() != sql_formatted.strip():
                warnings = True
                cell_id = cell['metadata']['id']
                logging.warning(
                    f'{filename}: Incorrectly formatted SQL in cell {cell_id}. To correct the formatting, run '
                    './manage.py format-sql-cells. Alternatively, locate the cell in Google Colaboratory by adding '
                    f'#scrollTo={cell_id} to the notebook URL and replace the cell contents with:\n\n'
                    f'{source[0]}\n{sql_formatted}')

    if warnings:
        sys.exit(1)


if __name__ == '__main__':
    cli()
