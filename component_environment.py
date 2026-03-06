# ## Setup
#
# *You must run the cells in this section each time you connect to a new runtime. For example, when you return to the notebook after an idle timeout, when the runtime crashes, or when you restart or factory reset the runtime.*

# Install requirements (*Note: ocdskingfishercolab installs google-colab, which expects specific versions of pandas and numpy*):
#

# ! pip install --upgrade pip > pip.log
# ! pip install --upgrade ocdskingfishercolab ipywidgets psycopg2-binary >> pip.log

# +
# @title Import packages and load extensions { display-mode: "form" }

import gzip
import json
import os
import shutil
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from google.colab.data_table import DataTable
from google.colab.files import download
from ipywidgets import widgets
from ocdskingfishercolab import (
    authenticate_gspread,
    calculate_coverage,
    download_dataframe_as_csv,
    format_thousands,
    render_json,
    save_dataframe_to_sheet,
    save_dataframe_to_spreadsheet,
    set_dark_mode,
    set_light_mode,
)

# Load https://pypi.org/project/ipython-sql/
# %load_ext sql
# Load https://colab.research.google.com/notebooks/data_table.ipynb
# %load_ext google.colab.data_table

# +
# @title Configure the notebook environment { display-mode: "form" }

# Increase max columns so that Pandas DataFrames with many columns are rendered as data tables.
DataTable.max_columns = 50
# Remove the index from data tables for easier copy-pasting to Google Docs.
DataTable.include_index = False

# Return Pandas DataFrames instead of regular result sets.
# %config SqlMagic.autopandas = True
# Don't print number of rows affected.
# %config SqlMagic.feedback = False

# If you set Tools > Settings > Site > Theme to dark, uncomment this line.
# set_dark_mode()
# If you are creating plots to copy-paste into reports, uncomment this line.
# set_light_mode()
