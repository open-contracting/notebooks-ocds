# ## Setup Kingfisher Process

# ### Connect to the database

# +
import getpass

from ocdskingfishercolab import (
    list_collections,
    list_source_ids,
    set_search_path,
)

# -

# Enter your PostgreSQL credentials and connect to the Kingfisher Process database:

user = input("Username:")
password = getpass.getpass("Password:")
connection_string = (
    "postgresql://"
    + user
    + ":"
    + password
    + "@postgres.kingfisher.open-contracting.org/kingfisher_process?sslmode=require"
)
# Don't show connection string after execute.
# %config SqlMagic.displaycon = False
# %sql $connection_string

# ### Choose collections and schema
#
# *Use this section to choose the collections and schema that you want to query.*

# #### Set the collection(s)

# Update `collection_ids` with the `id`(s) of the [Kingfisher Process collection(s)](https://kingfisher-process.readthedocs.io/en/latest/data-model.html#collections):

collection_ids = (2358, 2359)

# If you don't know which collections you need, run the next cell and use the **Filter** button to filter the [collection table](https://kingfisher-process.readthedocs.io/en/latest/database-structure.html#collection-table) to find the collection(s). You can use the `source_id` column to filter on the `name` of the [Kingfisher Collect spider](https://kingfisher-collect.readthedocs.io/en/latest/spiders.html) used to collect the data. Use the value(s) from the `id` column to update the previous cell.

list_collections()

# #### Set the schema

# Update `schema_name` with the name of the [Kingfisher Summarize schema](https://kingfisher-summarize.readthedocs.io/en/latest/index.html#how-it-works).

schema_name = "view_data_collection_2358_2359"
set_search_path(schema_name)

# If you don't know which schema you need, run the next cell and use the **Filter** button to filter the [selected collections table](https://kingfisher-summarize.readthedocs.io/en/latest/database.html#summaries-selected-collections) to find the schema. You can use the `collection_id` column to filter on the `id` of the collections that you identified in the previous step. Alternatively, you can filter on the `source_id` column. Use the value from the `schema` column to update the previous cell.

# + language="sql"
# SELECT
#     summaries.selected_collections.*,
#     source_id
# FROM
#     summaries.selected_collections
# INNER JOIN
#     collection
#     ON summaries.selected_collections.collection_id = collection.id
#
# -

# If you can't find a schema containing the collections that you want to query, you can create a schema using [Kingfisher Summarize](https://ocdsdeploy.readthedocs.io/en/latest/use/kingfisher-summarize.html).
