# OCDS Notebooks

A collection of Jupyter notebooks for working with data from:

- [Kingfisher Process](https://kingfisher-process.readthedocs.io/en/latest/)
- [Data Registry](https://data.open-contracting.org)
- Field lists, like from a [field-level mappings](https://www.open-contracting.org/resources/ocds-field-level-mapping-template/)

**Note:** If you encounter unfamiliar errors, try the *Runtime > Disconnect and delete runtime*  menu item. If the error still occurs, please [open an issue](https://github.com/open-contracting/kingfisher-colab/issues/new).

## Notebooks

To use a notebook:

* Click the *Open In Colab* button
* Click the *File > Save a copy in Drive* menu item
* Make your changes (e.g. `collection_ids`, `schema_name`, etc.)

If you make any improvements or fixes, please follow the *Contributing* guide below to merge your changes back into this repository.

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

To ease maintenance, the notebooks are made up of reusable components. To see which components are used in each notebook, refer to the `NOTEBOOKS` variable in `manage.py`.

**Reminder:** If you edit the *Check structure and format* or *Check quality* components and change the headings or add new sections, check whether the related *Document template* in this [process note](https://docs.google.com/document/d/1_k7eA2rI-k5EH8VESkVAB73wa_qrpplL-7dKgMLTGZc/edit) needs an update.

Use the buttons below to open the components from the `main` branch for editing in Google Colaboratory (Colab).

To open a component from a different branch, use Colab's [GitHub browser](https://colab.research.google.com/github/open-contracting/notebooks-ocds).

To encourage reuse, limit the scope of a component. The current scopes are:

- *Environment*: Setup Google Colaboratory in general.
- *Setup*: Setup Google Colaboratory for a data source.
- *Errors*: Review any issues in loading the data.
- *Scope*: Understand the scope of the data.
- *Check*: Perform a category of checks.

### Scopes

#### Environment

Component name | Open in Colab | Tasks
-- | -- | --
[Environment](https://github.com/open-contracting/notebooks-ocds/blob/main/component_environment.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_environment.ipynb) | Install requirements, import packages, load extensions and configure the notebook.

#### Setup

Component name | Open in Colab | Tasks
-- | -- | --
[Cardinal setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_cardinal.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_cardinal.ipynb) | Install Cardinal requirements, define coverage functions and calculate the field list for a given file.
[Charts setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_charts.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_charts.ipynb) | Install charts requirements, import charts packages and define plot functions.
[Kingfisher Process setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_kingfisher.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_kingfisher.ipynb) | Connect to the database. Choose the collection(s) and schema to work with.
[Field list setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_fieldlist.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_fieldlist.ipynb) | Load the field list.
[Data Registry download data setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_download_data_from_registry.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_download_data_from_registry.ipynb) | Define the functions to list publications and download JSONL files from the registry.
[Usability setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_usability.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_usability.ipynb) | Define the usability functions.
[Red flags setup](https://github.com/open-contracting/notebooks-ocds/blob/main/component_setup_red_flags.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_setup_red_flags.ipynb) | Define the red flags functions.

#### Errors

Component name | Open in Colab | Tasks
-- | -- | --
[Kingfisher Process errors](https://github.com/open-contracting/notebooks-ocds/blob/main/component_errors_kingfisher.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_errors_kingfisher.ipynb) | Check for data collection and processing errors.

#### Scope

Component name | Open in Colab | Tasks
-- | -- | --
[Structure scope](https://github.com/open-contracting/notebooks-ocds/blob/main/component_scope_kingfisher.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_scope_kingfisher.ipynb) | Check how many releases and records your data contains. Check the date range and stages of the contracting process covered by your data.
[Usability scope](https://github.com/open-contracting/notebooks-ocds/blob/main/component_scope_usability.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_scope_usability.ipynb) | Calculate general statistics.

#### Check

Component name | Open in Colab | Tasks
-- | -- | --
[Structure checks](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_structure.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_structure.ipynb) | Check for structure and format errors reported by [lib-cove-ocds](https://github.com/open-contracting/lib-cove-ocds).
[Conformance checks](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_conformance.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_conformance.ipynb) | Check against the [OCDS conformance criteria](https://standard.open-contracting.org/latest/en/schema/conformance_and_extensions/#publication-conformance).
[Quality checks](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_quality.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_quality.ipynb) | Check for conformance and quality issues that require manual review.
[Usability checks using Kingfisher with coverage](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_usability_kingfisher.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_usability_kingfisher.ipynb) |
[Usability checks using a field list without coverage](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_usability_external.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_usability_external.ipynb) | 
[Relevant checks using a field list](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_relevant.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_relevant.ipynb) | Given a field list, check if the list pass the "relevant" criteria. 
[Relevant checks against all the publications from the Data Registry](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_relevant_all_registry.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_relevant_all_registry.ipynb) | Downloads all the publications from the registry and performs the "relevant" checks against the active ones.
[Red flags checks using a field list without coverage](https://github.com/open-contracting/notebooks-ocds/blob/main/component_check_red_flags_external.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_check_red_flags_external.ipynb) | 

#### Other

Component name | Open in Colab | Tasks
-- | -- | --
[Data Registry download data](https://github.com/open-contracting/notebooks-ocds/blob/main/component_select_data_from_registry.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_select_data_from_registry.ipynb) | Define the forms to select a publication and year and download the selected publication.
[Get fields used by registered publications](https://github.com/open-contracting/notebooks-ocds/blob/main/component_get_field_list_all_registry.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/component_get_field_list_all_registry.ipynb) | Get the fields used by all OCDS publications in the Registry.

### Add a component

1. [Create a new notebook](https://colab.research.google.com/#create=true)
2. Set a title using H2 formatting and add your cells, following the [style guide for SQL statements](https://ocp-software-handbook.readthedocs.io/en/latest/services/postgresql.html#sql-statements).

### Edit a component

1. Open the component in Colab.
2. Add or edit cells, following the [style guide for SQL statements](https://ocp-software-handbook.readthedocs.io/en/latest/services/postgresql.html#sql-statements).

### Commit your changes

1. [Create a branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository#creating-a-branch).

In Colab:

1. Click Edit -> Clear all outputs.
1. Click File -> Save.
1. Select the 'notebooks-ocds' repository.
1. Select your branch, enter a commit message and click OK.
1. Uncheck 'Include a link to Colab'

### Add new components to a notebook

1. Add the component to the entry for the notebook in the `NOTEBOOKS` variable in `manage.py`.

### Add a new notebook

1. Add an entry for the the notebook and its components to the `NOTEBOOKS` variable in `manage.py`.
4. Update the 'Notebooks' section of `README.md`.

### Request a review

1. [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
2. Request a review from a data support manager.
3. If the reviewer requests changes, make the changes then repeat this step.

### Merge your changes

Once approved, you can merge your own changes.

## Reviewing

### Review changes

[Review the changes](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request).

For small changes, you can review the raw diff in the GitHub review interface.

For larger changes, you can review and comment on a visual diff by clicking the <img align="absmiddle"  alt="ReviewNB" height="28" class="BotMessageButtonImage" src="https://raw.githubusercontent.com/ReviewNB/support/master/images/button_reviewnb.png"/> button. You need to authorize the app the first time you open it.

# Maintenance

## Format SQL cells and merge components to build notebooks:

1. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

1. Install the pre-commit script:

    ```bash
    pre-commit install
    ```
