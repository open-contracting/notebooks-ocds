# ## Relevance analysis
#
# Use this section to assess if the publication contains the required fields to answer "who bought what from whom, for how much, when and how" for some subset of contracting processes.
#
# Generate a list of the fields published:

fields_list = fields_table.iloc[:, 0].tolist()

relevant, result = is_relevant(fields_list)

# ### Does the publication pass the relevant criterion?

relevant

# ### Why?

result

# ### Manually check for other fields
#
# If the main OCDS fields are not available to answer the relevant question, you should manually check if others might be used instead. This involves not only checking for the existence of a field but its content too. For example:
# - If you cannot answer "who", you could check if they disclose "buyer" or "procuringEntity" roles as part of the parties array.
# - If you cannot answer "from whom", you could check if they disclose the "supplier" role as part of the parties array.
#
# If a quick check yields no alternative field, do not spend more time. If you cannot easily find the relevant field, neither will another user.

fields_table

# #### Save the table to a spreadsheet

spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, result, "relevant table")
