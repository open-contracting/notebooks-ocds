# ## Select a publication from the [Data Registry](https://data.open-contracting.org/) and its field list

# +
# @title Select the publication to download { display-mode: "form" }

publication_select_box = get_publication_select_box()

publication_select_box

# +
# @title Extract the list of available fields { display-mode: "form" }

selected_publication = next(entry for entry in get_publications() if entry["label"] == publication_select_box.value)
fields_table = format_coverage(selected_publication.get("coverage", {}))
