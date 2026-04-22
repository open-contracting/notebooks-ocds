# ## Usability analysis setup
#
# Use this section to setup the functions needed to perform a usability analysis of the dataset, to identify if a publisher has the necessary fields to calculate 71 procurement indicators related to market opportunity (market description, competition, supplier performance), value for money, internal efficiency, public integrity and service delivery.  For an OCDS publisher, it also calculates the proportion of unique procedures for which it is possible to calculate the indicator (coverage).
#
# The usability checks includes all the indicators listed on [OCP's use case guide](https://docs.google.com/spreadsheets/d/1j-Y0ktZiOyhZzi-2GSabBCnzx6fF5lv8h1KYwi_Q9GM/edit#gid=1183427361) and the [Indicators to diagnose the performance of a procurement market document](https://docs.google.com/document/d/1vSJk9-qWSTQEx9ZZc7BUhQZMHvTRcyDYVS2sl8HB__k/edit#heading=h.nrnq1ajwwpqe).

# +
# @title Usability functions { display-mode: "form" }

RELEVANT_RULES = {
    "who": [
        "buyer/id",
        "buyer/name",
        "tender/procuringEntity/id",
        "tender/procuringEntity/name",
    ],
    "bought what": [
        "tender/items/classification/id",
        "awards/items/classification/id",
        "contracts/items/classification/id",
        "tender/items/classification/description",
        "awards/items/classification/description",
        "contracts/items/classification/description",
        "tender/items/description",
        "awards/items/description",
        "contracts/items/description",
        "tender/description",
        "awards/description",
        "contracts/description",
        "tender/title",
        "awards/title",
        "contracts/title",
    ],
    "from whom": [
        "awards/suppliers/id",
        "awards/suppliers/name",
    ],
    "for how much": [
        "awards/value/amount",
        "contracts/value/amount",
        [
            "awards/items/quantity",
            "awards/items/unit/value/amount",
        ],
        [
            "contracts/items/quantity",
            "contracts/items/unit/value/amount",
        ],
    ],
    "when": [
        "tender/tenderPeriod/endDate",
        "awards/date",
        "contracts/dateSigned",
    ],
    "how": [
        "tender/procurementMethod",
        "tender/procurementMethodDetails",
    ],
}


def check_usability_indicators(lang, result):
    # Use case guide: Indicators linked to OCDS #public
    if lang.value == "English":
        spreadsheet_key = "1j-Y0ktZiOyhZzi-2GSabBCnzx6fF5lv8h1KYwi_Q9GM"
    else:  # [ES]
        spreadsheet_key = "1l_p_e1iNUUuR5AObTJ8EY9VrcCLTAq3dnG_Fj73UH9w"

    rows = authenticate_gspread().open_by_key(spreadsheet_key).get_worksheet(0).get_all_values()
    indicators = pd.DataFrame(rows).pipe(lambda df: df.rename(columns=df.iloc[0]).drop(df.index[0]))

    if lang.value == "English":
        return result.merge(indicators.iloc[:, [0, 3, 4, 9]], on="U_id")

    return (
        indicators.iloc[:, [0, 3, 4, 5, 9]]
        .merge(result, on="U_id")
        .drop(columns="indicator")
        .rename(
            columns={
                "fields needed": "Campos necesarios",
                "calculation": "¿Se puede calcular?",
                "missing fields": "Campos faltantes",
                "coverage": "Cobertura",
            }
        )
        .replace({"¿Se puede calcular?": {"possible to calculate": "sí", "missing fields": "campos faltantes"}})
    )


def is_relevant(field_list):
    """
    Check if the dataset has the basic fields to answer: who bought what, from whom, for how much, when, and how.

    Each rule in RELEVANT_RULES is satisfied if ANY of its options is present:
    - String options: the field must be in field_list
    - List options: all fields in the list must be in field_list
    """
    results = []
    for rule_name, options in RELEVANT_RULES.items():
        available = []
        missing = []
        possible = False

        for option in options:
            if isinstance(option, str):
                if option in field_list:
                    available.append(option)
                    possible = True
                else:
                    missing.append(option)
            else:
                all_present = True
                for opt in option:
                    if opt in field_list:
                        available.append(opt)
                    else:
                        missing.append(opt)
                        all_present = False
                if all_present:
                    possible = True

        results.append(
            {
                "rule": rule_name,
                "possible_to_calculate": "Yes" if possible else "No",
                "available_fields": available,
                "missing_fields": missing,
            }
        )

    df = pd.DataFrame(results)
    return (df["possible_to_calculate"] == "Yes").all(), df
