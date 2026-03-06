#!/usr/bin/env python
import zlib
from pathlib import Path

import click
import jupytext
import nbformat
import sqlfluff
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
        "component_setup_metadadata_from_registry",
        "component_select_data_from_registry",
        "component_setup_usability",
        "component_check_usability_external",
    ],
    "template_relevant_checks_registry": [
        "component_environment",
        "component_setup_usability",
        "component_setup_metadadata_from_registry",
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
        "component_setup_usability",
        "component_setup_metadadata_from_registry",
        "component_check_relevant_all_registry",
    ],
    "template_red_flags_checks_registry": [
        "component_environment",
        "component_setup_metadadata_from_registry",
        "component_select_data_from_registry",
        "component_setup_red_flags",
        "component_check_red_flags_external",
    ],
    "template_red_flags_checks": [
        "component_environment",
        "component_setup_kingfisher",
        "component_setup_red_flags",
        "component_check_red_flags_kingfisher",
    ],
    "template_red_flags_checks_fieldlist": [
        "component_environment",
        "component_setup_fieldlist",
        "component_setup_red_flags",
        "component_check_red_flags_external",
    ],
    "template_field_list_registry_all": [
        "component_environment",
        "component_setup_metadadata_from_registry",
        "component_get_field_list_all_registry",
    ],
}

BASEDIR = Path(__file__).resolve().parent
FLUFF_CONFIG = FluffConfig.from_path(BASEDIR)
MAIN_LANGUAGE_HEADER = "---\njupyter:\n  jupytext:\n    main_language: python\n---\n"


def get_component_path(name):
    for extension in (".py", ".md"):
        path = BASEDIR / f"{name}{extension}"
        if path.exists():
            return path
    raise FileNotFoundError(name)


@click.command()
@click.argument("filename", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def pre_commit(filename):
    """Format SQL cells in component notebooks and merge components to build template notebooks."""
    has_warnings = False

    changed = {path.stem for path in filename if path.name.startswith("component_")}

    templates = []
    needed = set()
    for slug, component_names in NOTEBOOKS.items():
        if any(name in changed for name in component_names):
            templates.append(slug)
            needed.update(component_names)

    components = {}
    for name in needed:
        path = get_component_path(name)
        content = path.read_text()
        if path.suffix == ".md":
            content = f"{MAIN_LANGUAGE_HEADER}{content}"
        notebook = jupytext.reads(content, fmt={"extension": path.suffix, "split_at_heading": True})

        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue

            source = cell.source.splitlines(keepends=True)

            # In our notebooks, this is always on its own line: %%sql(?!( \w+ <<)?\\n",)
            if "%%sql" not in source[0]:
                continue

            fix = sqlfluff.fix("".join(source[1:]), config=FLUFF_CONFIG)
            cell.source = [source[0], *fix.splitlines(keepends=True)]

            warnings = sqlfluff.lint(fix, config=FLUFF_CONFIG)
            has_warnings |= bool(warnings)

            for warning in warnings:
                click.secho(f"{warning['code']}:{warning['name']} {warning['description']}", fg="yellow")
                if "start_file_pos" in warning:
                    start = warning["start_file_pos"]
                    end = warning["end_file_pos"]
                    click.echo(f"{fix[:start]}{click.style(fix[start:end], fg='red')}{fix[end:]}")

        components[name] = notebook

    for slug in templates:
        merged = nbformat.v4.new_notebook()
        merged.metadata["colab"] = {"toc_visible": True}  # default False
        for name in NOTEBOOKS[slug]:
            merged.cells.extend(components[name].cells)

        # Assign deterministic cell IDs based on content hash.
        for i, cell in enumerate(merged.cells):
            source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
            cell.id = format(zlib.crc32(f"{i}:{source}".encode()) & 0xFFFFFFFF, "08x")

        with (BASEDIR / f"{slug}.ipynb").open("w") as f:
            nbformat.write(merged, f)

    if has_warnings:
        raise click.Abort


if __name__ == "__main__":
    pre_commit()
