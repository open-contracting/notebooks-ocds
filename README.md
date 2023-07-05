# Kingfisher Notebooks

A collection of Jupyter notebooks for working with data in [Kingfisher Process](https://kingfisher-process.readthedocs.io/en/latest/).

## Notebooks

To use a notebook:

* Click the *Open In Colab* button
* Click the *File > Save a copy in Drive* menu item
* Make your changes (e.g. `collection_ids`, `schema_name`, etc.)

If you make any improvements or fixes, please follow the *Contributing* guide below to merge your changes back into this repository.

You can also use a notebook without creating a copy. However, if you re-open the notebook, any changes and outputs will be lost.

Notebook | Open in Colab | Description
-- | -- | --
[Publisher analysis template](https://github.com/open-contracting/notebooks-ocds/blob/main/publisher_analysis_template.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/publisher_analysis_template.ipynb) | Use this notebook to analyse data from a specific publisher 
[Meta analysis template](https://github.com/open-contracting/notebooks-ocds/blob/main/meta_analysis_template.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/meta_analysis_template.ipynb) | Use this notebook to analyse data from multiple publishers, or to perform other types of analysis on the Kingfisher database
[Structure and format feedback template](https://github.com/open-contracting/notebooks-ocds/blob/main/structure_and_format_feedback_template.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/structure_and_format_feedback_template.ipynb) | Use this notebook to provide feedback on structure and format issues reported by the Data Review Tool
[Data quality feedback template](https://github.com/open-contracting/notebooks-ocds/blob/main/data_quality_feedback_template.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/notebooks-ocds/blob/main/data_quality_feedback_template.ipynb) | Use this notebook to provide detailed feedback on structure, format, conformance and coherence issues 
Usability checks template | | Use this notebook to provide feedback on data usability

## Contributing

### Components

To ease maintenance, the notebooks are made up of reusable components. To see which components are used in each notebook, refer to the `NOTEBOOKS` variable in `manage.py`.

**Reminder:** If you edit the *Check structure and format* or *Check quality* components and change the headings or add new sections, check whether the related *Document template* in this [process note](https://docs.google.com/document/d/1_k7eA2rI-k5EH8VESkVAB73wa_qrpplL-7dKgMLTGZc/edit) needs an update.

Component | Open in Colab | Tasks
-- | -- | --
[Setup environment](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/setup_environment.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/setup_environment.ipynb) | Install requirements, import functions, load extensions and set config. Connect to the Kingfisher database.
[Choose data](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/choose_data.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/choose_data.ipynb) | Choose a data source, collection and schema to work with.
[Check for errors](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/check_for_errors.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/check_for_errors.ipynb) | Check for data collection and processing errors.
[Check scope](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/check_scope.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/check_scope.ipynb) | Check how many releases and records your data contains. Check the date range and stages of the contracting process covered by your data.
[Check structure and format](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/check_structure_and_format.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/check_structure_and_format.ipynb) | Check for structure and format errors reported by the Data Review Tool.
[Check quality](https://github.com/open-contracting/kingfisher_notebook_components/blob/main/check_data_quality.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/blob/main/check_data_quality.ipynb) | Check for conformance and coherence errors.

Use the buttons above to open the components from the `main` branch for editing in Google Colaboratory (Colab).

To open a component from a different branch, use Colab's [GitHub browser](https://colab.research.google.com/github/open-contracting/kingfisher_notebook_components/).

Alternatively, you can use the Open in Colab browser extension ([Chrome](https://chrome.google.com/webstore/detail/open-in-colab/), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/open-in-colab/)) to add a button that, when clicked when viewing a Jupyter notebook on GitHub, will open that notebook in Colab.

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
1. Click File -> Save a copy in GitHub.
1. Uncheck 'Include a link to Colaboratory'
1. Select your branch, enter a commit message and click OK.

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

1. Install [pg_format](https://github.com/darold/pgFormatter).
2. Run `./manage.py pre-commit`.
