# ## Get the fields used by all OCDS publications in the Registry
#
# Use this notebook to get the list of the fields implemented by all the publishers in the Data Registry, for example, to check what publishers are publishing specific fields.

# ### Aggregate the lists of fields across all publications

# +
final_dataset = pd.DataFrame()

for publication in get_publications():
    data = format_coverage(publication.get("coverage", {}))
    data["publisher"] = publication["source_id"]
    final_dataset = pd.concat([final_dataset, data])
# -

final_dataset

# Export the results as CSV

final_dataset.to_csv("ocds_fields_from_all_publishers.csv", index=False)
