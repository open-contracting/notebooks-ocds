# ## Usability analysis
#
# Generate a list of the fields published:

fields_list = fields_table.iloc[:, 0].tolist()

result = usability_checks(fields_list)

# ### Export and visualize results

# #### Choose language of the export

lang = get_usability_language_select_box()
lang

# #### Load use case indicators spreadsheet

result_final = check_usability_indicators(lang, result)

# #### Table of results

result_final

# #### Save the table to a spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result_final, "usability table")

# #### Visualize results

plot_usability_indicators(result_final, lang.value)
