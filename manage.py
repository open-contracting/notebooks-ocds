#!/usr/bin/env python
import base64
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import click
from googleapiclient.discovery import MediaFileUpload, build
from oauth2client.service_account import ServiceAccountCredentials


def yield_notebooks():
    directory = Path(__file__).resolve().parent

    for filename in os.listdir(directory):
        if not filename.endswith('.ipynb'):
            continue

        filepath = os.path.join(directory, filename)
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
    Check that SQL cells in Jupyter Notebooks are formatted using pg_format.
    """
    warnings = False

    for filename, filepath, notebook in yield_notebooks():
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


@cli.command()
def upload():
    """
    Upload Jupyter Notebooks to Google Drive.

    The GOOGLE_SERVICE_ACCOUNT environment variable must be set.
    """
    GOOGLE_SERVICE_ACCOUNT = base64.b64decode(os.environ['GOOGLE_SERVICE_ACCOUNT']).decode('UTF-8')

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(GOOGLE_SERVICE_ACCOUNT),
        scopes=['https://www.googleapis.com/auth/drive']
    )

    service = build('drive', 'v3', credentials=credentials)

    files = [
        (
            '11Z3RAhI97Dan2usiuN5CUWwfJ23WLNob',
            'publisher_analysis_template.ipynb',
            'Publisher Analysis Template',
        ),
        (
            '1NXYvi3eHOWlFHXzcg7Vhw3xNJpNXcqx1',
            'setup_environment.ipynb',
            'Meta Analysis Template',
        ),
        (
            '1GmkA3kFL9k9MdTUln4pcRmc-KZneL5VB',
            'structure_and_format_feedback_template.ipynb',
            'Structure and Format Feedback Template',
        ),
        (
            '1Lj96xTde5GpFQ5hnvB2GYZ7gY4wuvUYt',
            'data_quality_feedback_template.ipynb',
            'Data Quality Feedback Template',
        ),
    ]

    for file_id, path, name in files:
        file = service.files().get(fileId=file_id).execute()

        del file['id']
        file['name'] = name

        media_body = MediaFileUpload(path, resumable=True)
        service.files().update(fileId=file_id, body=file, media_body=media_body).execute()


if __name__ == '__main__':
    cli()
