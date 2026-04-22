# ## Red flags analysis setup
#
# Use this section to setup the functions needed to perform a usability analysis of the dataset, to identify if a publisher has the necessary fields to calculate 73 red flags indicators.

# +
# @title Red flags functions { display-mode: "form" }


def check_red_flags_indicators(result):
    # NEW Red Flags to OCDS mapping #Public
    spreadsheet_key = "1GACSPd64X5Tm-nu6LKttyEpaEp1CLsaCUGrEutljnFU"
    rows = authenticate_gspread().open_by_key(spreadsheet_key).get_worksheet(1).get_all_values()
    indicators = pd.DataFrame(rows).pipe(lambda df: df.rename(columns=df.iloc[0]).drop(df.index[0]))
    return result.merge(indicators.iloc[:, [0, 5, 6, 7]], on="R_id")
