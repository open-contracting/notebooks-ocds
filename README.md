# OCDS Notebooks

A collection of Jupyter notebooks for working with data from:

- [Kingfisher Process](https://kingfisher-process.readthedocs.io/en/latest/)
- [Data Registry](https://data.open-contracting.org)
- Field lists, like from a [field-level mappings](https://www.open-contracting.org/resources/ocds-field-level-mapping-template/)

## Notebooks

To use a notebook:

* Click the *Open In Colab* button
* Click the *File > Save a copy in Drive* menu item
* Make your changes (e.g. `collection_ids`, `schema_name`, etc.)

If you encounter unfamiliar errors, try the *Runtime > Disconnect and delete runtime*  menu item. If the error still occurs, please [open an issue](https://github.com/open-contracting/kingfisher-colab/issues/new).

If you make any improvements or fixes, please follow the [Contributing guide](#contributing) below to merge your changes back into this repository.

You can also use a notebook without creating a copy. However, if you re-open the notebook, any changes and outputs will be lost.

### Kingfisher Process

Notebook | Open in Colab | Description
-- | -- | --
[Publisher analysis template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_publisher_analysis.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_publisher_analysis.ipynb) | Analyze data from a specific publisher.
[Meta analysis template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_meta_analysis.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_meta_analysis.ipynb) | Analyze data from multiple publishers, or to perform other types of analysis on the Kingfisher Process database.
[Basic criteria feedback template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_basic_criteria_checks.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_basic_criteria_checks.ipynb) | Provide feedback on the [OCDS basic criteria](https://standard.open-contracting.org/latest/en/guidance/publish/quality/#basic-criteria).
[Structure and format feedback template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_structure_and_format_feedback.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_structure_and_format_feedback.ipynb) | Provide feedback on structure and format errors reported by [lib-cove-ocds](https://github.com/open-contracting/lib-cove-ocds).
[Data quality feedback template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_data_quality_feedback.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_data_quality_feedback.ipynb) | Provide detailed feedback on structure, format, conformance and quality issues.
[Usability checks template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_usability_checks.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_usability_checks.ipynb) | Provide feedback on data usability for OCDS datasets.
[Red flags checks template](https://github.com/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks.ipynb) | Provide feedback on red flags for OCDS datasets.

### Other data sources

Notebook | Open in Colab | Description
-- | -- | --
[Usability checks using a field list](https://github.com/open-contracting/notebooks-ocds/blob/main/template_usability_checks_fieldlist.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_usability_checks_fieldlist.ipynb) | Provide feedback on data usability for prospective OCDS publishers, using a field list, like from a field-level mapping.
[Usability checks using the Data Registry](https://github.com/open-contracting/notebooks-ocds/blob/main/template_usability_checks_registry.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_usability_checks_registry.ipynb) | Provide feedback on data usability using data from the [Data Registry](https://data.open-contracting.org/).
[Relevant checks using a field list](https://github.com/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_fieldlist.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_fieldlist.ipynb) | Provide feedback on data relevance for prospective publishers, using a field list, like from a field-level mapping.
[Relevant checks using the Data Registry](https://github.com/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_registry.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_registry.ipynb) | Provide feedback on data relevance using data from the [Data Registry](https://data.open-contracting.org/).
[Relevant checks for all the Data Registry publications](https://github.com/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_registry_all.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_relevant_checks_registry_all.ipynb) | Provide feedback on data relevance downloading all the publications from the [Data Registry](https://data.open-contracting.org/).
[Red flags checks using the Data Registry](https://github.com/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks_registry.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks_registry.ipynb) | Provide feedback on coverage for red flags using data from the [Data Registry](https://data.open-contracting.org/).
[Red flags checks using a field list](https://github.com/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks_fieldlist.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_red_flags_checks_fieldlist.ipynb) | Provide feedback on red flags for prospective OCDS publishers, using a field list, like from a field-level mapping.
[Field list for all the Data Registry publications](https://github.com/open-contracting/notebooks-ocds/blob/main/template_field_list_registry_all.ipynb) | [![Open Iinn Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/template_field_list_registry_all.ipynb) | Extract the fields published by all the publications from the [Data Registry](https://data.open-contracting.org/).

## Contributing

### Components

To ease maintenance, the notebooks are made up of reusable components with clear scopes:

- **Environment**: Setup Google Colaboratory in general
  - `environment`: Install requirements, import packages, load extensions and configure the notebook.
- **Setup**: Setup Google Colaboratory for a data source
  - `setup_charts`: Install charts requirements, import charts packages and define plot functions.
  - `setup_kingfisher`: Connect to the Kingfisher Process database. Choose the collection(s) and schema to work with.
  - `setup_fieldlist`: Load the field list.
  - `setup_metadata_from_registry`: Define the functions to list publications and their metadata, including coverage, from the Registry.
  - `setup_usability`: Define the usability functions.
  - `setup_red_flags`: Define the red flags functions.
- **Errors**: Review any issues in loading the data
  - `errors_kingfisher`: Check for data collection (Kingfisher Collect) and processing (Kingfisher Process) errors.
- **Scope**: Understand the scope of the data
  - `scope_kingfisher`: Check how many releases and records your data contains. Check the date range and stages of the contracting process covered by your data.
  - `scope_usability`: Calculate general statistics.
- **Check**: Perform a category of checks
  - `check_structure`: Check for structure and format errors reported by [lib-cove-ocds](https://github.com/open-contracting/lib-cove-ocds).
  - `check_conformance`: Check against the [OCDS conformance criteria](https://standard.open-contracting.org/latest/en/schema/conformance_and_extensions/#publication-conformance).
  - `check_quality`: Check for conformance and quality issues that require manual review.
  - `check_usability_kingfisher`: Usability checks using Kingfisher with coverage.
  - `check_usability_external`: Usability checks using a field list without coverage.
  - `check_relevant`: Given a field list, check if the list pass the "relevant" criteria. 
  - `check_relevant_all_registry`: Performs the "relevant" checks against the active publications from the Registry.
  - `check_red_flags_external`: Red flags checks using a field list without coverage.
- **Other**
  - `select_data_from_registry`: Define the form to select a publication from the Registry.
  - `get_field_list_all_registry`: Get the fields used by all OCDS publications in the Registry.

### Quick reference

Follow the [style guide for SQL statements](https://ocp-software-handbook.readthedocs.io/en/latest/services/postgresql.html#sql-statements).

- To see which components are used in each notebook, refer to the `NOTEBOOKS` variable in `manage.py`.
- To add new components to a notebook, add to the entry for the notebook in the `NOTEBOOKS` variable in `manage.py`.
- To add a new notebook:
  - Add an entry for the the notebook and its components to the `NOTEBOOKS` variable in `manage.py`.
  - Update the [Notebooks section](#notebooks) of the `README.md`.

### Add a component using Colab

1. [Create a branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository#creating-a-branch).
1. [Create a new notebook](https://colab.research.google.com/#create=true)
1. Set a title using H2 formatting, and add your cells.
1. Commit your changes:
    - Click Edit -> Clear all outputs.
    - Click File -> Save.
    - Select the 'notebooks-ocds' repository.
    - Select your branch, enter a commit message and click OK.
    - Uncheck 'Include a link to Colab'
1. Request a review:
    - [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
    - Request a review from a data support manager.
    - If the reviewer requests changes, make the changes then repeat this step.
1. Once approved, you can merge your own changes.

### Add or edit a component using an editor

**Reminder:** If you change headings or add sections, check whether any related *Document template* in this [process note](https://docs.google.com/document/d/1_k7eA2rI-k5EH8VESkVAB73wa_qrpplL-7dKgMLTGZc/edit) needs an update.

[Jupytext](https://jupytext.readthedocs.io) is used to encode notebooks as Markdown files (if code cells are mostly SQL) or Python files.

Python files use the [light format](https://jupytext.readthedocs.io/en/latest/formats-scripts.html#the-light-format). For example:

```py
# ## A heading
#
# A paragraph

python_code = "cell"
second_line = "code"

another_code_cell = True
```

To merge code cells, use start-of-cell and end-of-cell delimiters:

```py
# +
code = "cell"

same = "cell"
# -
```

To [hide code](https://colab.research.google.com/notebooks/snippets/forms.ipynb):

```py
# +
# @title My title { display-mode: "form" }

python = "code"
# -
```

The end-of-cell delimiter is optional if the next cell is also hidden, or at the end of the file.

To add SQL:

```py
# + language="sql"
# SELECT 1
# -
```

Or:

```py
# + magic_args="my_variable <<" language="sql"
# SELECT 1
# -
```
