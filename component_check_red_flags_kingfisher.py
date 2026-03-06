# ## Usability analysis
#
# Generate a list of the fields published:

# + magic_args="fields_table <<" language="sql"
# SELECT
#     path,
#     distinct_releases
# FROM
#     field_counts
# WHERE
#     release_type = 'compiled_release'
# -

fields_list = fields_table.iloc[:, 0].tolist()

indicators_dict = get_red_flags_dictionary(fields_list)
result = redflags_checks(fields_list, indicators_dict, check_coverage=True)
result["coverage"] = get_coverage(indicators_dict)

# ### Export results

# #### Load use case indicators spreadsheet

result_final = check_red_flags_indicators(result)

# #### Table of results

result_final

# #### Most common fields for indicators
#
# This table shows the most frequent fields used to calculate indicators and if they are published.  You can use this table to highlight to the publisher the key data gaps.

common_fields = most_common_fields_to_calculate_indicators(indicators_dict, fields_table)
common_fields

# #### Save tables to spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result_final, "red_flags_table")
save_dataframe_to_sheet(spreadsheet_name, common_fields, "common_fields_table")
save_dataframe_to_sheet(spreadsheet_name, fields_table, "fields_list")
