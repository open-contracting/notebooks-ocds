# Kingfisher Notebooks

A collection of components and templates for working with data in OCDS Kingfisher using Jupyter notebooks.

## Components

The notebook components in this repository are the single source of truth for common tasks performed by OCDS Helpdesk analysts. Use the buttons below to open the components from the `main` branch for editing in Google Colaboratory (Colab):

Component | Tasks
-- | --
[Setup environment](https://github.com/duncandewhurst/kingfisher_notebook_components/blob/main/setup_environment.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duncandewhurst/kingfisher_notebook_components/blob/main/setup_environment.ipynb) | Install requirements, import functions, load extensions and set config. Connect to the Kingfisher database.
[Choose data](https://github.com/duncandewhurst/kingfisher_notebook_components/blob/main/choose_data.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duncandewhurst/kingfisher_notebook_components/blob/main/choose_data.ipynb) | Choose a data source, collection and schema to work with.
[Check for errors](https://github.com/duncandewhurst/kingfisher_notebook_components/blob/main/data_collection_and_processing_errors.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duncandewhurst/kingfisher_notebook_components/blob/main/data_collection_and_processing_errors.ipynb) | Check for data collection and processing errors.

To open a component from a different branch, use Colab's [Github browser](https://colab.research.google.com/github/duncandewhurst/kingfisher_notebook_components/) to choose the component and branch you want to open.

Alternatively, you can use the Open in Colab browser extension ([Chrome](https://chrome.google.com/webstore/detail/open-in-colab/), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/open-in-colab/)) to add a button that, when clicked when viewing a Jupyter notebook on Github, will open that notebook in Colab.

## Templates

Each time a component is updated, Github Actions builds template notebooks from the components and writes them to a [Google Drive folder](https://drive.google.com/drive/u/0/folders/1eb3pSQ55HylMsmwKqu7MrkvH12ROD4-9).

The following table describes the relationship between the templates and components. Use the links to open the templates in [Google Colaboratory](https://colab.research.google.com/) and then save a copy to use in your analysis.

Template | Description | Setup environment | Choose data | Check for errors
-- | -- | -- | -- | --
[Publisher analysis template](https://drive.google.com/file/d/1R-VBYA-SC9CoMIdvYp_SI9V2UFWlTqx0/view?usp=sharing)[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1R-VBYA-SC9CoMIdvYp_SI9V2UFWlTqx0) | Use to analyse data from a specific publisher | <ul><li>- [x]</li></ul> | <ul><li>- [x]</li></ul> | <ul><li>- [x]</li></ul>
[Meta analysis template]() | Use to analyse data from multiple publishers | <ul><li>- [x]</li></ul> | <ul><li>- []</li></ul> | <ul><li>- []</li></ul>
[Data feedback template]() | Use to provide feedback on data quality | <ul><li>- []</li></ul> | <ul><li>- []</li></ul> | <ul><li>- []</li></ul>
[Usability checks template]() | Use to provide feedback on data usability | <ul><li>- []</li></ul> | <ul><li>- []</li></ul> | <ul><li>- []</li></ul>

## Contributing

### Edit a component

1. Open the component in Colab.

2. Make your changes in Colab, following the [style guide for SQL statements](https://ocp-software-handbook.readthedocs.io/en/latest/python/code.html#sql-statements).

3. Format any SQL code you add or edit using [pgFormatter](http://sqlformat.darold.net/).

### Commit your changes

1. [Create a branch](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-and-deleting-branches-within-your-repository#creating-a-branch).

In Colab:

2. Click Edit -> Clear all outputs.

3. Click File -> Save a copy in Github.

4. Uncheck 'Include a link to Colaboratory'

5. Select your branch, enter a commit message and click OK.

### Request a review

1. [Create a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

2. Request a review from a helpdesk analyst.

3. If the reviewer requests changes, make the changes then repeat this step.

### Merge your changes

Once approved, you can merge your changes yourself.

## Reviewing

### Review changes

[Review the changes](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/reviewing-proposed-changes-in-a-pull-request).

For small changes, you can review the raw diff in the Github review interface.

For larger changes, you can review and comment on a visual diff by clicking the <img align="absmiddle"  alt="ReviewNB" height="28" class="BotMessageButtonImage" src="https://raw.githubusercontent.com/ReviewNB/support/master/images/button_reviewnb.png"/> button. You need to authorize the app the first time you open it.
