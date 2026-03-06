# ## Usability analysis setup
#
# Use this section to setup the functions needed to perform a usability analysis of the dataset, to identify if a publisher has the necessary fields to calculate 71 procurement indicators related to market opportunity (market description, competition, supplier performance), value for money, internal efficiency, public integrity and service delivery.  For an OCDS publisher, it also calculates the proportion of unique procedures for which it is possible to calculate the indicator (coverage).
#
# The usability checks includes all the indicators listed on [OCP's use case guide](https://docs.google.com/spreadsheets/d/1j-Y0ktZiOyhZzi-2GSabBCnzx6fF5lv8h1KYwi_Q9GM/edit#gid=1183427361) and the [Indicators to diagnose the performance of a procurement market document](https://docs.google.com/document/d/1vSJk9-qWSTQEx9ZZc7BUhQZMHvTRcyDYVS2sl8HB__k/edit#heading=h.nrnq1ajwwpqe).

# +
# @title Usability functions { display-mode: "form" }

# Repeated requirements.
BUYER_RULE = {
    "any": [
        {"all": ["buyer/name", "buyer/id"]},
        {"all": ["tender/procuringEntity/name", "tender/procuringEntity/id"]},
        {"all": ["parties/identifier/name", "parties/identifier/id", "parties/roles"]},
    ]
}
TENDERERS_RULE = {
    "any": [
        "tender/tenderers/id",
        "bids/details/tenderers/id",
    ]
}
ITEM_CLASSIFICATIONS_RULE = {
    "any": [
        {"all": ["tender/items/classification/id", "tender/items/classification/scheme"]},
        {"all": ["awards/items/classification/id", "awards/items/classification/scheme"]},
        {"all": ["contracts/items/classification/id", "contracts/items/classification/scheme"]},
    ]
}
AWARDS_WITH_VALUES_RULE = {
    "any": [
        {"all": ["contracts/id", "contracts/status", "contracts/value/amount", "contracts/value/currency"]},
        {"all": ["awards/id", "awards/status", "awards/value/amount", "awards/value/currency"]},
    ]
}
TENDERERS_COUNT_RULE = {
    "any": [
        "tender/numberOfTenderers",
        "tender/tenderers/id",
        "bids/details/tenderers/id",
    ]
}
AWARDS_WITH_ITEMS_RULE = {
    "any": [
        {
            "all": [
                "awards/status",
                "awards/value/amount",
                "awards/value/currency",
                "awards/items/classification/id",
                "awards/items/classification/scheme",
            ]
        },
        {
            "all": [
                "contracts/status",
                "contracts/value/amount",
                "contracts/value/currency",
                "contracts/items/classification/id",
                "contracts/items/classification/scheme",
            ]
        },
    ]
}
TENDER_VALUE_RULE = {
    "any": [
        {"all": ["planning/budget/amount/amount", "planning/budget/amount/currency"]},
        {"all": ["tender/value/amount", "tender/value/currency"]},
    ]
}

# Indicators as (name, rule) tuples.
# {"all": [...]} means all sub-requirements are needed (logical AND).
# {"any": [...]} means at least one sub-requirement is needed (logical OR).
INDICATORS = {
    "U001": (
        "Total number of procedures",
        {"all": ["ocid"]},
    ),
    "U002": (
        "Total number of procuring entities",
        {"all": ["ocid", BUYER_RULE]},
    ),
    "U003": (
        "Total number of unique bidders",
        {"all": ["ocid", TENDERERS_RULE]},
    ),
    "U004": (
        "Total number of awarded suppliers",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", "awards/status"]},
    ),
    "U005": (
        "Total number of procedures by year or month",
        {"all": ["ocid", "date"]},
    ),
    "U006": (
        "Total value awarded",
        {"all": ["ocid", "awards/status", "awards/value/amount", "awards/value/currency"]},
    ),
    "U007": (
        "Share of procedures by status",
        {"all": ["ocid", "tender/status"]},
    ),
    "U008": (
        "Number of procedures by item type",
        {"all": ["ocid", ITEM_CLASSIFICATIONS_RULE]},
    ),
    "U009": (
        "Proportion of procedures by procurement category",
        {"all": ["ocid", "tender/mainProcurementCategory"]},
    ),
    "U010": (
        "Percent of tenders by procedure type",
        {"all": ["ocid", "tender/procurementMethod"]},
    ),
    "U011": (
        "Percent of tenders awarded by means of competitive procedures",
        {"all": ["ocid", "tender/procurementMethod", "awards/status"]},
    ),
    "U012": (
        "Percent of contracts awarded under each procedure type",
        {
            "all": [
                "ocid",
                "tender/procurementMethod",
                {"any": [{"all": ["contracts/id", "contracts/status"]}, {"all": ["awards/id", "awards/status"]}]},
            ]
        },
    ),
    "U013": (
        "Total contracted value awarded under each procedure type",
        {"all": ["ocid", "tender/procurementMethod", AWARDS_WITH_VALUES_RULE]},
    ),
    "U014": (
        "Total awarded value of tenders awarded by means of competitive procedures",
        {"all": ["ocid", "tender/procurementMethod", AWARDS_WITH_VALUES_RULE]},
    ),
    "U015": (
        "Proportion of single bid tenders",
        {"all": ["ocid", "tender/procurementMethod", TENDERERS_COUNT_RULE]},
    ),
    "U016": (
        "Proportion of value awarded in single bid tenders vs competitive tenders",
        {
            "all": [
                "ocid",
                "tender/procurementMethod",
                "awards/status",
                "awards/value/amount",
                "awards/value/currency",
                TENDERERS_COUNT_RULE,
            ]
        },
    ),
    "U017": (
        "Mean number of bidders per tender",
        {"all": ["ocid", "tender/procurementMethod", TENDERERS_COUNT_RULE]},
    ),
    "U018": (
        "Median number of bidders per tender",
        {"all": ["ocid", "tender/procurementMethod", TENDERERS_COUNT_RULE]},
    ),
    "U019": (
        "Mean number of bidders by item type",
        {"all": ["ocid", "tender/procurementMethod", TENDERERS_COUNT_RULE, ITEM_CLASSIFICATIONS_RULE]},
    ),
    "U020": (
        "Number of suppliers by item type",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", ITEM_CLASSIFICATIONS_RULE]},
    ),
    "U021": (
        "Number of new bidders in a system",
        {"all": ["tender/id", "tender/tenderers/id", "tender/tenderPeriod/startDate"]},
    ),
    "U022": (
        "Percent of new bidders to all bidders",
        {"all": ["tender/id", "tender/tenderers/id", "tender/tenderPeriod/startDate"]},
    ),
    "U023": (
        "Percent of tenders with at least three participants deemed qualified",
        {"all": ["ocid", "bids/details/tenderers/id", "bids/details/id", "bids/details/status"]},
    ),
    "U024": (
        "Mean percent of bids which are disqualified",
        {"all": ["tender/id", "bids/details/id", "bids/details/status"]},
    ),
    "U025": (
        "Percent of contracts awarded to top 10 suppliers with largest contracted totals",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", AWARDS_WITH_VALUES_RULE]},
    ),
    "U026": (
        "Mean number of unique suppliers per buyer",
        {"all": ["ocid", "awards/suppliers/id", "awards/suppliers/name", BUYER_RULE]},
    ),
    "U027": (
        "Number of new awarded suppliers",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", "awards/date"]},
    ),
    "U028": (
        "Percent of awards awarded to new suppliers",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", "awards/date"]},
    ),
    "U029": (
        "Total awarded value awarded to new suppliers",
        {
            "all": [
                "awards/id",
                "awards/suppliers/id",
                "awards/suppliers/name",
                "awards/date",
                "awards/value/amount",
                "awards/value/currency",
            ]
        },
    ),
    "U030": (
        "Percent of new suppliers to all suppliers",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", "awards/date"]},
    ),
    "U031": (
        "Percent of growth of new awarded suppliers in a system",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", "awards/date"]},
    ),
    "U032": (
        "Percent of total awarded value awarded to recurring suppliers",
        {
            "all": [
                "awards/id",
                "awards/suppliers/id",
                "awards/suppliers/name",
                "awards/date",
                "awards/value/amount",
                "awards/value/currency",
            ]
        },
    ),
    "U033": (
        "Mean number of bids necessary to win",
        {"all": ["ocid", "tender/tenderers/id", "awards/suppliers/id", "awards/suppliers/name"]},
    ),
    "U034": (
        "Market concentration, market share of the largest company in the market",
        {"all": ["awards/suppliers/id", "awards/suppliers/name", AWARDS_WITH_ITEMS_RULE]},
    ),
    "U035": (
        "Proportion of contracts awarded by supplier by non competitive procedures",
        {"all": ["ocid", "tender/procurementMethod", "awards/status", "awards/suppliers/id", "awards/suppliers/name"]},
    ),
    "U036": (
        "Region of the supplier",
        {"all": ["parties/roles", "parties/identifier/id", "parties/address/region"]},
    ),
    "U037": (
        "Number of bids submitted by supplier",
        {"all": ["awards/suppliers/id", TENDERERS_RULE]},
    ),
    "U038": (
        "Success rate of bidders",
        {"all": ["ocid", "tender/tenderers/id", "awards/suppliers/id", "awards/suppliers/name"]},
    ),
    "U039": (
        "Number of unique items classifications awarded by supplier",
        {"all": ["awards/id", "awards/suppliers/id", "awards/suppliers/name", ITEM_CLASSIFICATIONS_RULE]},
    ),
    "U040": (
        "Total value awarded by supplier",
        {"all": ["awards/suppliers/id", "awards/suppliers/name", AWARDS_WITH_VALUES_RULE]},
    ),
    "U041": (
        "Share of total value awarded by supplier",
        {"all": ["awards/suppliers/id", "awards/suppliers/name", AWARDS_WITH_VALUES_RULE]},
    ),
    "U042": (
        "Total number of contracts awarded by supplier",
        {
            "all": [
                "awards/id",
                "awards/suppliers/id",
                "awards/suppliers/name",
                {"any": ["awards/status", "contracts/status"]},
            ]
        },
    ),
    "U043": (
        "Number of procuring entities by supplier",
        {"all": ["ocid", "awards/suppliers/id", "awards/suppliers/name", BUYER_RULE]},
    ),
    "U044": (
        "Share of single bid awards by supplier",
        {
            "all": [
                "ocid",
                "awards/suppliers/id",
                "awards/suppliers/name",
                "awards/status",
                "tender/procurementMethod",
                TENDERERS_COUNT_RULE,
            ]
        },
    ),
    "U045": (
        "Percent of tenders with linked procurement plans",
        {"all": ["tender/id", "tender/documents/documentType"]},
    ),
    "U046": (
        "Percent of contracts which publish information on debarments",
        {"all": ["contracts/id", "contracts/implementation/documents/documentType"]},
    ),
    "U047": (
        "The percent of tenders for which the tender documentation was added after publication of the announcement",
        {"all": ["tender/id", "tender/documents/documentType", "tender/documents/datePublished"]},
    ),
    "U048": (
        "Mean number of contract amendments per buyer",
        {"all": ["ocid", "contracts/id", "contracts/amendments", BUYER_RULE]},
    ),
    "U049": (
        "Percent of tenders which have been closed for more than 30 days, but whose basic awards information is not published",
        {
            "all": [
                "tender/id",
                "tender/tenderPeriod/endDate",
                "awards/id",
                "awards/date",
                "awards/status",
                "awards/value/amount",
                "awards/suppliers/id",
                "awards/suppliers/name",
            ]
        },
    ),
    "U050": (
        "Percent of awards which are older than 30 days, but whose contract is not published",
        {
            "all": [
                "awards/id",
                "awards/date",
                "contracts/awardID",
                "contracts/status",
                "contracts/dateSigned",
                "contracts/documents/documentType",
            ]
        },
    ),
    "U051": (
        "Percent of tenders that do not specify place of delivery",
        {"all": ["ocid", "tender/items/deliveryLocation", "tender/items/deliveryAddress"]},
    ),
    "U052": (
        "Percent of tenders that do not specify date of delivery",
        {
            "all": [
                "tender/milestones/id",
                "tender/milestones/type",
                "tender/milestones/description",
                "tender/milestones/dueDate",
            ]
        },
    ),
    "U053": (
        "Percent of tenders with short titles for example fewer than 10 characters in the title",
        {"all": ["tender/id", "tender/title"]},
    ),
    "U054": (
        "Percent of tenders with short descriptions for instance fewer than 30 characters in the description",
        {"all": ["tender/id", "tender/description"]},
    ),
    "U055": (
        "Percent of tenders that do not include detailed item codes or item descriptions",
        {"all": ["tender/id", "tender/items/classification/id", "tender/items/classification/scheme"]},
    ),
    "U056": (
        "Percent of contracts that do not have amendments",
        {"all": ["contracts/id", "contracts/amendments"]},
    ),
    "U057": (
        "Percent of contracts which publish contract implementation details financial",
        {
            "all": [
                "contracts/implementation/transactions/id",
                "contracts/implementation/transactions/value/amount",
                "contracts/implementation/transactions/value/currency",
            ]
        },
    ),
    "U058": (
        "Percent of contracts which publish contract implementation details physical",
        {
            "all": [
                "contracts/implementation/milestones/type",
                "contracts/implementation/milestones/id",
                "contracts/implementation/milestones/dueDate",
                "contracts/implementation/milestones/status",
            ]
        },
    ),
    "U059": (
        "Average duration of tendering period days",
        {"all": ["ocid", "tender/tenderPeriod/startDate", "tender/tenderPeriod/endDate"]},
    ),
    "U060": (
        "Average duration of decision period days",
        {"all": ["ocid", "tender/tenderPeriod/endDate", "awards/date"]},
    ),
    "U061": (
        "Average days from award date to start of implementation",
        {
            "all": [
                "awards/id",
                "awards/date",
                {"any": ["contracts/period/startDate", "awards/contractPeriod/startDate"]},
            ]
        },
    ),
    "U062": (
        "Days between award date and tender start date",
        {"all": ["ocid", "tender/tenderPeriod/startDate", "awards/date"]},
    ),
    "U063": (
        "Percent of canceled tenders to awarded tenders",
        {"all": ["ocid", "tender/status", "awards/status"]},
    ),
    "U064": (
        "Percent of contracts which are canceled",
        {"all": ["contracts/id", "contracts/status"]},
    ),
    "U065": (
        "Price variation of same item across all awards",
        {
            "all": [
                AWARDS_WITH_ITEMS_RULE,
                {
                    "any": [
                        {"all": ["awards/items/quantity", "awards/items/unit"]},
                        {"all": ["contracts/items/quantity", "contracts/items/unit"]},
                    ]
                },
            ]
        },
    ),
    "U066": (
        "Percent of contracts that exceed budget",
        {"all": ["ocid", "contracts/status", "contracts/value/amount", "contracts/value/currency", TENDER_VALUE_RULE]},
    ),
    "U067": (
        "Mean percent overrun of contracts that exceed budget",
        {"all": ["ocid", "contracts/status", "contracts/value/amount", "contracts/value/currency", TENDER_VALUE_RULE]},
    ),
    "U068": (
        "Total percent savings difference between budget and contract value",
        {
            "all": [
                "ocid",
                "planning/budget/amount/amount",
                "planning/budget/amount/currency",
                "contracts/value/amount",
                "contracts/value/currency",
            ]
        },
    ),
    "U069": (
        "Total percent savings difference between tender value estimate and contract value",
        {
            "all": [
                "ocid",
                "tender/value/amount",
                "tender/value/currency",
                "contracts/value/amount",
                "contracts/value/currency",
            ]
        },
    ),
    "U070": (
        "Percent of contracts completed on time",
        {"all": ["contracts/id", "contracts/period/endDate", "contracts/status"]},
    ),
    "U071": (
        "Share of contracts whose milestones are completed on time",
        {
            "all": [
                "contracts/id",
                "contracts/implementation/milestones/dueDate",
                "contracts/implementation/milestones/dateMet",
            ]
        },
    ),
}

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


def _evaluate_rule(rule, fields_list):
    """
    Evaluate a DSL rule against a list of available fields.

    Rules can be:
    - A string: the field must be present in fields_list
    - {"all": [...]}: all sub-rules must be satisfied (logical AND)
    - {"any": [...]}: at least one sub-rule must be satisfied (logical OR)

    Returns True if the rule is satisfied, False otherwise.
    """
    if isinstance(rule, str):
        return rule in fields_list
    if isinstance(rule, dict):
        if "all" in rule:
            return all(_evaluate_rule(sub_rule, fields_list) for sub_rule in rule["all"])
        if "any" in rule:
            return any(_evaluate_rule(sub_rule, fields_list) for sub_rule in rule["any"])
    return False


def _get_required_fields(rule):
    """
    Extract all field names from a DSL rule for display purposes.

    For "any" rules, shows the first option's fields as the representative requirement.
    """
    if isinstance(rule, str):
        return [rule]
    if isinstance(rule, dict):
        if "all" in rule:
            fields = []
            for sub_rule in rule["all"]:
                fields.extend(_get_required_fields(sub_rule))
            return fields
        if rule.get("any"):
            # Return the first option as the representative
            return _get_required_fields(rule["any"][0])
    return []


def _get_missing_fields(rule, fields_list):
    """
    Get the missing fields for a DSL rule.

    For "any" rules, returns missing fields from the option that has the fewest missing fields.
    """
    if isinstance(rule, str):
        return [rule] if rule not in fields_list else []
    if isinstance(rule, dict):
        if "all" in rule:
            missing = []
            for sub_rule in rule["all"]:
                missing.extend(_get_missing_fields(sub_rule, fields_list))
            return missing
        if "any" in rule:
            # Find the option with the fewest missing fields
            best_missing = None
            for sub_rule in rule["any"]:
                sub_missing = _get_missing_fields(sub_rule, fields_list)
                if not sub_missing:
                    return []  # Found a satisfied option
                if best_missing is None or len(sub_missing) < len(best_missing):
                    best_missing = sub_missing
            return best_missing or []
    return []


def usability_checks(fields_list):
    """
    Return a table of the usability checks.

    It indicates if the fields needed to calculate a particular indicator are present.
    """
    return pd.DataFrame(
        [
            {
                "indicator": name,
                "U_id": u_id,
                "fields needed": ", ".join(_get_required_fields(rule)),
                "calculation": "possible to calculate" if _evaluate_rule(rule, fields_list) else "missing fields",
                "missing fields": ", ".join(_get_missing_fields(rule, fields_list)),
            }
            for u_id, (name, rule) in INDICATORS.items()
        ]
    )


def check_usability_indicators(lang, result):
    # Use case guide: Indicators linked to OCDS #public
    if lang.value == "English":
        spreadsheet_key = "1j-Y0ktZiOyhZzi-2GSabBCnzx6fF5lv8h1KYwi_Q9GM"
    else:  # [ES]
        spreadsheet_key = "1l_p_e1iNUUuR5AObTJ8EY9VrcCLTAq3dnG_Fj73UH9w"

    rows = authenticate_gspread().open_by_key(spreadsheet_key).sheet1.get_all_values()
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


def get_coverage():
    """Calculate coverage for each indicator using DSL rules."""
    return [
        pd.to_numeric(calculate_coverage(_get_required_fields(rule), "release_summary")["total_percentage"][0])
        for _name, rule in INDICATORS.values()
    ]


def most_common_fields_to_calculate_indicators(fields_table):
    """Count the most common fields used across all indicators using DSL rules."""
    fields_count = (
        pd.DataFrame.from_dict(
            Counter(field for _name, rule in INDICATORS.values() for field in _get_required_fields(rule)),
            orient="index",
        )
        .reset_index()
        .rename(columns={"index": "field", 0: "number of indicators"})
        .sort_values("number of indicators", ascending=False)
        .reset_index(drop=True)
    )
    fields_count["published"] = np.where(fields_count["field"].isin(fields_table["path"]), "yes", "no")
    return fields_count


def get_usability_language_select_box():
    return widgets.Dropdown(
        options=["Spanish", "English"], description="language", style={"description_width": "initial"}
    )
