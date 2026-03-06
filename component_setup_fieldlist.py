# ## Setup field list

# To run this notebook, you need to have the list of fields that the publisher is intended to publish. You can get that list from their mapping template. We currently don't have an automatic way to extract the list from the template, so you must get this list manually.
#
# Upload an Excel file that includes the list of fields available in a column (no header).  Change the name of the file below. The list of fields must have the object/field_name format, for example `tender/id`.

file_name = "ADD FILE"

# Transform the file into a dataframe
#

fields_table = pd.read_excel(file_name, header=None, names=["path", "count"])
fields_list = fields_table.iloc[:, 0].tolist()
fields_table
