#!/usr/bin/env python
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import click
from nbformat import reads
from nbformat import write as write_notebook
from nbmerge import merge_notebooks

# A dict of notebooks and their components, identified by filename, excluding '.ipynb'
NOTEBOOKS = {
    'meta_analysis_template': [
        'setup_environment',
    ],
    'publisher_analysis_template': [
        'setup_environment',
        'choose_data',
        'check_scope',
    ],
    'structure_and_format_feedback_template': [
        'setup_environment',
        'choose_data',
        'check_scope',
        'check_structure_and_format',
    ],
    'data_quality_feedback_template': [
        'setup_environment',
        'choose_data',
        'check_scope',
        'check_structure_and_format',
        'check_data_quality',
    ]}

BASEDIR = Path(__file__).resolve().parent


def yield_notebooks():
    for filename in os.listdir(BASEDIR):
        if not filename.endswith('.ipynb'):
            continue

        filepath = os.path.join(BASEDIR, filename)
        with open(filepath, 'r') as f:
            notebook = json.load(f)

        yield filename, filepath, notebook


def yield_cells(notebook):
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue

        source = cell['source']
        if '%%sql' not in source[0]:
            continue

        sql = ''.join(source[1:])
        pg_format = subprocess.run(['pg_format', '-f', '1'], input=sql, stdout=subprocess.PIPE, check=True,
                                   universal_newlines=True)

        yield source, cell, sql, pg_format.stdout


def build_notebook(slug):
    return merge_notebooks(BASEDIR, [f'{c}.ipynb' for c in NOTEBOOKS[slug]], False, None)


@click.group()
def cli():
    pass


@cli.command()
def pre_commit():
    """
    Format SQL cells in Jupyter Notebooks using pg_format and merge components to build notebooks.
    """

    for filename, filepath, notebook in yield_notebooks():
        for source, cell, sql, sql_formatted in yield_cells(notebook):
            cell['source'] = [source[0], "\n"] + sql_formatted.splitlines(keepends=True)

        with open(filepath, 'w') as f:
            json.dump(notebook, f, ensure_ascii=False, indent=2)
            f.write('\n')

    for slug in NOTEBOOKS:
        with open(f'{slug}.ipynb', 'w', encoding='utf8') as f:
            write_notebook(build_notebook(slug), f)


@cli.command()
def check():
    """
    Check that notebooks and components are in sync, and SQL cells in Jupyter Notebooks are formatted using pg_format.
    """
    warnings = False

    for filename, filepath, notebook in yield_notebooks():
        slug = filename.split('.')[0]
        if slug in NOTEBOOKS:
            built_notebook = build_notebook(slug)
            if reads(json.dumps(notebook), as_version=4) != built_notebook:
                warnings = True
                logging.warning(
                    f'{filename}: Mismatch between the notebook and its components. If you edited a component, run '
                    './manage.py pre-commit to update the notebook. If you edited the notebook, replicate your '
                    ' changes in the relevant components.')

        for source, cell, sql, sql_formatted in yield_cells(notebook):
            if sql.strip() != sql_formatted.strip():
                warnings = True
                cell_id = cell['metadata']['id']
                logging.warning(
                    f'{filename}: Incorrectly formatted SQL in cell {cell_id}. To correct the formatting, run '
                    './manage.py pre-commit. Alternatively, locate the cell in Google Colaboratory by adding '
                    f'#scrollTo={cell_id} to the notebook URL and replace the cell contents with:\n\n'
                    f'{source[0]}\n{sql_formatted}')

    if warnings:
        sys.exit(1)


if __name__ == '__main__':
    cli()
