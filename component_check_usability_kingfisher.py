# ## Usability analysis
#
# Generate a list of the fields published:

fields_list = set(fields_table["path"])
indicators = load_indicators(prefix="U")
result = indicator_checks(fields_list, indicators)
result = result.rename(columns={"id": "U_id"})
result["coverage"] = get_coverage(fields_list, indicators)

# ### Export and visualize results

# #### Choose language of the export

lang = widgets.Dropdown(options=["Spanish", "English"], description="language", style={"description_width": "initial"})
lang

# #### Load use case indicators spreadsheet

result_final = check_usability_indicators(lang, result)

# #### Table of results

result_final

# #### Most common fields for indicators
#
# This table shows the most frequent fields used to calculate indicators and if they are published.  You can use this table to highlight to the publisher the key data gaps.

fields_count = most_common_fields_to_calculate_indicators(fields_list, indicators)
fields_count

# #### Save tables to spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result_final, "usability table")
save_dataframe_to_sheet(spreadsheet_name, fields_count, "key fields")

# #### Visualize results

plot_usability_indicators(result_final, lang.value)
