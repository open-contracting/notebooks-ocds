# ## Usability analysis
#
# Generate a list of the fields published:

fields_list = set(fields_table["path"])
indicators = load_indicators(prefix="U")
result = indicator_checks(fields_list, indicators)
result = result.rename(columns={"id": "U_id"})

# ### Export and visualize results

# #### Choose language of the export

lang = widgets.Dropdown(options=["Spanish", "English"], description="language", style={"description_width": "initial"})
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
