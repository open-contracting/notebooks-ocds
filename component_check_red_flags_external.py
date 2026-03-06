# ## Usability analysis

# Generate a list of the fields published:

fields_list = fields_table.iloc[:, 0].tolist()

indicators_dic = get_red_flags_dictionary(fields_list)
result = redflags_checks(fields_list, indicators_dic)

# ### Export results

# #### Load use case indicators spreadsheet

result_final = check_red_flags_indicators(result)

# #### Table of results

result_final

# #### Results summary

table = result_final.groupby("calculation").agg(total_red_flags=("R_id", "count")).reset_index()
table["%"] = round(table["total_red_flags"] / table["total_red_flags"].sum() * 100, 1)
table

# #### Most common fields to indicators

common_fields = most_common_fields_to_calculate_indicators(indicators_dic, fields_table)
common_fields

# #### Save the table to a spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result_final, "red_flags_table")
save_dataframe_to_sheet(spreadsheet_name, common_fields, "common_fields_table")
save_dataframe_to_sheet(spreadsheet_name, fields_table, "fields_list")
