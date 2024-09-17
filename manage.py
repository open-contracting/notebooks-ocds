#!/usr/bin/env python
import json
import os
import subprocess
from pathlib import Path

import click
import jsonschema
from nbformat import write as write_notebook
from nbmerge import merge_notebooks

# A dict of notebooks and their components, identified by filename, excluding '.ipynb'
NOTEBOOKS = {
    "template_meta_analysis": [
        "component_environment",
        "component_setup_kingfisher",
    ],
    "template_publisher_analysis": [
        "component_environment",
        "component_setup_charts",
        "component_setup_kingfisher",
        "component_errors_kingfisher",
        "component_scope_kingfisher",
    ],
    "template_structure_and_format_feedback": [
        "component_environment",
        "component_setup_charts",
        "component_setup_kingfisher",
        "component_errors_kingfisher",
        "component_check_conformance",
        "component_scope_kingfisher",
        "component_check_structure",
    ],
    "template_data_quality_feedback": [
        "component_environment",
        "component_setup_charts",
        "component_setup_kingfisher",
        "component_errors_kingfisher",
        "component_check_conformance",
        "component_scope_kingfisher",
        "component_check_structure",
        "component_check_quality",
    ],
    "template_usability_checks": [
        "component_environment",
        "component_setup_charts",
        "component_setup_kingfisher",
        "component_scope_usability",
        "component_setup_usability",
        "component_check_usability_kingfisher",
    ],
    "template_usability_checks_fieldlist": [
        "component_environment",
        "component_setup_charts",
        "component_setup_fieldlist",
        "component_setup_usability",
        "component_check_usability_external",
    ],
    "template_usability_checks_registry": [
        "component_environment",
        "component_setup_charts",
        "component_setup_cardinal",
        "component_setup_download_data_from_registry",
        "component_select_data_from_registry",
        "component_setup_usability",
        "component_check_usability_external",
    ],
    "template_relevant_checks_registry": [
        "component_environment",
        "component_setup_cardinal",
        "component_setup_usability",
        "component_setup_download_data_from_registry",
        "component_select_data_from_registry",
        "component_check_relevant",
    ],
    "template_relevant_checks_fieldlist": [
        "component_environment",
        "component_setup_fieldlist",
        "component_setup_usability",
        "component_check_relevant",
    ],
    "template_basic_criteria_checks": [
        "component_environment",
        "component_setup_charts",
        "component_setup_usability",
        "component_setup_kingfisher",
        "component_errors_kingfisher",
        "component_check_structure",
        "component_check_conformance",
        "component_scope_usability",
        "component_check_relevant",
    ],
    "template_relevant_checks_registry_all": [
        "component_environment",
        "component_setup_cardinal",
        "component_setup_usability",
        "component_setup_download_data_from_registry",
        "component_check_relevant_all_registry",
    ],
}

BASEDIR = Path(__file__).resolve().parent


class InvalidNotebookError(click.ClickException):
    def __init__(self, filename):
        super().__init__(f"{filename} is invalid")


def yield_notebooks():
    for entry in os.scandir(BASEDIR):
        if not entry.name.endswith(".ipynb"):
            continue

        path = Path(entry.path)
        with path.open() as f:
            try:
                notebook = json.load(f)
            except json.decoder.JSONDecodeError as e:
                raise InvalidNotebookError(path) from e

        yield entry.name, path, notebook


def yield_cells(notebook):
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue

        source = cell["source"]
        if "%%sql" not in source[0]:
            continue

        sql = "".join(source[1:])
        pg_format = subprocess.run(  # noqa: S603 # trusted input
            ["pg_format", "-f", "1"],  # noqa: S607
            input=sql,
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        )

        yield source, cell, sql, pg_format.stdout


def build_notebook(slug):
    try:
        notebook = merge_notebooks(BASEDIR, [f"{c}.ipynb" for c in NOTEBOOKS[slug]], verbose=False)
        notebook["metadata"]["colab"]["name"] = slug
    except jsonschema.exceptions.ValidationError as e:
        raise InvalidNotebookError(f"{slug}.ipynb") from e
    else:
        return notebook


def json_dump(path, notebook):
    with path.open("w") as f:
        # Use indent=2 like Google Colab for small diffs.
        json.dump(notebook, f, ensure_ascii=False, indent=2)
        f.write("\n")


@click.command()
@click.argument("filename", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def pre_commit(filename):
    """Format SQL cells in Jupyter Notebooks using pg_format and merge components to build notebooks."""
    resolved = [path.resolve() for path in filename]

    for _, filepath, notebook in yield_notebooks():
        if not resolved or filepath.resolve() in resolved:
            for source, cell, _, sql_formatted in yield_cells(notebook):
                cell["source"] = [source[0], "\n", *sql_formatted.splitlines(keepends=True)]

        json_dump(filepath, notebook)

    for slug in NOTEBOOKS:
        filepath = Path(f"{slug}.ipynb")
        with filepath.open("w", encoding="utf8") as f:
            write_notebook(build_notebook(slug), f)
        # nbformat uses indent=1.
        with filepath.open() as f:
            notebook = json.load(f)
        json_dump(filepath, notebook)


if __name__ == "__main__":
    pre_commit()
