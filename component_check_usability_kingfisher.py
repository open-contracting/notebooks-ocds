# ## Usability analysis

# Generate a list of the fields published:

fields_list = fields_table.iloc[:, 0].tolist()

indicators_dict = get_indicators_dictionary(fields_list)
result = usability_checks(fields_list, indicators_dict)
result["coverage"] = get_coverage(indicators_dict)

# ### Export and visualize results

# #### Choose language of the export

lang = get_usability_language_select_box()
lang

# #### Load use case indicators spreadsheet

result_final = check_usability_indicators(lang, result)

# #### Table of results

result_final

# #### Most common fields for indicators

# This table shows the most frequent fields used to calculate indicators and if they are published.  You can use this table to highlight to the publisher the key data gaps.

fields_count = most_common_fields_to_calculate_indicators(indicators_dict, fields_table)
fields_count

# #### Save tables to spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result_final, "usability table")
save_dataframe_to_sheet(spreadsheet_name, fields_count, "key fields")

# #### Visualize results

plot_usability_indicators(result_final, lang.value)
