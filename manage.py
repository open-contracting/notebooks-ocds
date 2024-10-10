#!/usr/bin/env python
import json
from pathlib import Path

import click
import jsonschema
import nbformat
import sqlfluff
from nbmerge import merge_notebooks
from sqlfluff.core import FluffConfig

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
FLUFF_CONFIG = FluffConfig.from_path(BASEDIR)


class InvalidNotebookError(click.ClickException):
    def __init__(self, filename):
        super().__init__(f"{filename} is invalid")


def json_dump(path, notebook):
    with path.open("w") as f:
        # Use indent=2 like Google Colab for small diffs.
        json.dump(notebook, f, ensure_ascii=False, indent=2)
        f.write("\n")


def json_load(path):
    with path.open() as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as e:
            raise InvalidNotebookError(path) from e


@click.command()
@click.argument("filename", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def pre_commit(filename):
    """Format SQL cells in Jupyter Notebooks and merge components to build notebooks."""
    has_warnings = False

    filenames = [path for path in filename if path.name.startswith("component_")]

    for path in filenames:
        notebook = json_load(path)

        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue

            source = cell["source"]

            # In our notebooks, this is always on its own line: %%sql(?!( \w+ <<)?\\n",)
            if "%%sql" not in source[0]:
                continue

            fix = sqlfluff.fix("".join(source[1:]), config=FLUFF_CONFIG)
            cell["source"] = [source[0], *fix.splitlines(keepends=True)]

            warnings = sqlfluff.lint(fix, config=FLUFF_CONFIG)
            has_warnings |= bool(warnings)

            for warning in warnings:
                click.secho(f"{warning['code']}:{warning['name']} {warning['description']}", fg="yellow")
                if "start_file_pos" in warning:
                    start = warning["start_file_pos"]
                    end = warning["end_file_pos"]
                    click.echo(f"{fix[:start]}{click.style(fix[start:end], fg='red')}{fix[end:]}")

        json_dump(path, notebook)

    for slug, components in NOTEBOOKS.items():
        if any(path.stem in components for path in filenames):
            template_path = Path(f"{slug}.ipynb")

            with template_path.open("w", encoding="utf8") as f:
                try:
                    notebook = merge_notebooks(BASEDIR, [f"{c}.ipynb" for c in NOTEBOOKS[slug]], verbose=False)
                    notebook["metadata"]["colab"]["name"] = slug
                except jsonschema.exceptions.ValidationError as e:
                    raise InvalidNotebookError(f"{slug}.ipynb") from e
                else:
                    nbformat.write(notebook, f)

            # nbformat.write() uses indent=1. Rewrite with indent=2 like Google Colab.
            # https://github.com/jupyter/nbformat/blob/ba2c6f5/nbformat/v4/nbjson.py#L51
            json_dump(template_path, json_load(template_path))

    if has_warnings:
        raise click.Abort


if __name__ == "__main__":
    pre_commit()
