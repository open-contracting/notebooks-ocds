# ## Check the MVP status of the Data registry publications
#
# Use this notebook to check which publications in the Data Registry pass the MVP Relevant and Active criteria, for example, for updating the MEL1 tracker upon OCP Rapid Reflection meetings.

# +
# @title Get all the publications from the registry { display-mode: "form" }

publications = get_publications()
# -

# ### Check for non-frozen publications whose latest data has not been updated in the previous four calendar quarters
#
# From the list, check also the "last_retrieved" and "update_frequency" columns. If the data is not being retrieved, check the publication log in the Data Registry to check if there is a problem with either a job or the source data itself.

non_frozen_publications = [item for item in publications if not item["frozen"] and item["date_to"]]
today = datetime.now(tz=timezone.utc)
past_year = today - relativedelta(years=1)
lapsed_publications = [
    item
    for item in non_frozen_publications
    if datetime.strptime(item["date_to"], "%Y-%m-%d").astimezone(timezone.utc) < past_year
]
lapsed_publications_table = pd.DataFrame(lapsed_publications)
lapsed_publications_table

# ### Check non-relevant publications
# Check which active publications pass and not pass the "Relevant" criterion.

results = []
active_publications = [item for item in non_frozen_publications if item not in lapsed_publications]
for publication in active_publications:
    field_table = format_coverage(publication.get("coverage", {}))
    fields_list = field_table.iloc[:, 0].tolist()
    relevant, relevant_table = is_relevant(fields_list)
    relevant_table["publisher"] = publication["label"]
    relevant_table["relevant"] = relevant
    results.append(relevant_table)

# Filter the non-relevant ones

result = pd.concat(results)
not_relevant_publishers = result[~result["relevant"]]
non_relevant_rules = (
    not_relevant_publishers[not_relevant_publishers["possible_to_calculate"] == "No"]
    .groupby("publisher")
    .apply(lambda x: ", ".join(x["rule"].astype(str) + ": " + x["missing_fields"].astype(str)))
    .reset_index()
    .rename(columns={0: "failed rules"})
)

# Check the results

non_relevant_rules
