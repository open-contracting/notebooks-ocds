#!/usr/bin/env python
import click
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

directory = Path(__file__).resolve().parent


@click.group()
def cli():
    pass


@cli.command()
def format_sql_cells():
    """
    Format SQL cells in Jupyter Notebooks using pg_format.
    """ 
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # Ignore files that aren't notebooks
        if filename.endswith('.ipynb'):
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r') as f:
                notebook = json.load(f)

            for cell in notebook['cells']:

                if cell['cell_type'] == 'code':
                    source = cell['source']

                    # Ignore non-SQL cells
                    if '%%sql' in source[0]:
                        sql = ''.join(source[1:])
                        pg_format = subprocess.run(['pg_format', '-f', '1'], input=sql, capture_output=True, text=True)
                        sql_formatted = pg_format.stdout
                        cell['source'] = [source[0], "\n"] + sql_formatted.splitlines(keepends=True)

            with open(filepath, 'w') as f:
                json.dump(notebook, f, indent=2)


@cli.command()
def check_sql_cells():
    """
    Check that SQL cells are formatted using pg_format
    """
    
    warnings = False
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # Ignore files that aren't notebooks
        if filename.endswith('.ipynb'):
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r') as f:
                notebook = json.load(f)

            for cell in notebook['cells']:

                if cell['cell_type'] == 'code':
                    source = cell['source']

                    # Ignore non-SQL cells
                    if '%%sql' in source[0]:
                        sql = ''.join(source[1:])
                        pg_format = subprocess.run(['pg_format', '-f', '1'], input=sql, capture_output=True, text=True)
                        sql_formatted = pg_format.stdout

                        if sql.strip() != sql_formatted.strip():
                            warnings = True
                            cell_id = cell['metadata']['id']
                            logging.warning(f'{filename}: Incorrectly formatted SQL in cell {cell_id}. To correct the formatting, run ./manage.py format_sql_cells. Alternatively, locate the cell in Google Colaboratory by adding #scrollTo={cell_id} to the notebook URL and replace the cell contents with:\n\n{source[0]}\n{sql_formatted}')

    if warnings:
        sys.exit(-1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    cli()
