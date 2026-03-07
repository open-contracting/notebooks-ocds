# ## Red flags analysis setup
#
# Use this section to setup the functions needed to perform a usability analysis of the dataset, to identify if a publisher has the necessary fields to calculate 73 red flags indicators.

# +
# @title Red flags functions { display-mode: "form" }

# Repeated requirements.
BUYER_RULE = {
    "any": [
        {"all": ["buyer/name", "buyer/id"]},
        {"all": ["tender/procuringEntity/name", "tender/procuringEntity/id"]},
        {"all": ["parties/name", "parties/id", "parties/roles"]},
    ]
}

TENDERERS_RULE = {"any": ["tender/tenderers/id", "bids/details/tenderers/id"]}

TENDERERS_COUNT_RULE = {
    "any": [
        "tender/numberOfTenderers",
        "tender/tenderers/id",
        "bids/details/tenderers/id",
        "bids/statistics/value",
    ]
}

AWARDS_OR_CONTRACTS_RULE = {
    "any": [
        {"all": ["awards/status", "awards/date", "awards/value/amount", "awards/value/currency"]},
        {"all": ["contracts/status", "contracts/dateSigned", "contracts/value/amount", "contracts/value/currency"]},
    ]
}

ITEM_CLASSIFICATIONS_RULE = {
    "any": [
        {"all": ["tender/items/classification/id", "tender/items/classification/scheme"]},
        {"all": ["awards/items/classification/id", "awards/items/classification/scheme"]},
        {"all": ["contracts/items/classification/id", "contracts/items/classification/scheme"]},
    ]
}

UNIT_ITEMS_RULE = {
    "any": [
        {"all": ["tender/items/unit/value/amount", "tender/items/unit/value/currency"]},
        {"all": ["awards/items/unit/value/amount", "awards/items/unit/value/currency"]},
        {"all": ["contracts/items/unit/value/amount", "contracts/items/unit/value/currency"]},
    ]
}

DATE_RULE = {"any": ["tender/tenderPeriod/startDate", "awards/date"]}

AMOUNT_RULE = {
    "any": [
        "tender/value/amount",
        "bids/details/value/amount",
        "awards/value/amount",
        "contracts/value/amount",
    ]
}

WINNING_BID_RULE = {
    "any": [
        {"all": ["awards/relatedBid"]},
        {"all": ["bids/details/tenderers/id", "awards/suppliers/id"]},
    ]
}

BIDDERS_INFO_RULE = {
    "any": [
        "parties/contactPoint/telephone",
        "parties/address/streetAddress",
        "parties/address/postalCode",
    ]
}

CONTACT_INFO_RULE = {
    "any": [
        "parties/contactPoint/telephone",
        "parties/contactPoint/email",
        "parties/contactPoint/name",
    ]
}

IMPLEMENTATION_VALUE_RULE = {
    "any": [
        {"all": ["contracts/implementation/finalValue/amount", "contracts/implementation/finalValue/currency"]},
        {
            "all": [
                "contracts/implementation/transactions/value/amount",
                "contracts/implementation/transactions/value/currency",
            ]
        },
    ]
}

# Indicators as (name, rule) tuples.
# {"all": [...]} means all sub-requirements are needed (logical AND).
# {"any": [...]} means at least one sub-requirement is needed (logical OR).
RED_FLAGS = {
    "R001": ("Planning documents not available", {"all": ["planning/documents/documentType"]}),
    "R002": (
        "Manipulation of procurement thresholds",
        {
            "all": [
                "tender/value/amount",
                "tender/value/currency",
                "tender/procurementMethod",
                "tender/tenderPeriod/startDate",
                BUYER_RULE,
            ]
        },
    ),
    "R003": (
        "The submission period is too short",
        {"all": ["tender/tenderPeriod/startDate", "tender/tenderPeriod/endDate", "tender/procurementMethod"]},
    ),
    "R004": (
        "Failure to adequately advertise the request for bids",
        {"all": ["tender/documents/documentType", "tender/documents/datePublished", "tender/tenderPeriod/startDate"]},
    ),
    "R005": (
        "Key tender information and documents are not available",
        {
            "all": [
                "tender/documents/documentType",
                "tender/documents/datePublished",
                "tender/tenderPeriod/startDate",
                "tender/tenderPeriod/endDate",
            ]
        },
    ),
    "R006": ("Unreasonable prequalification requirements", {"all": ["tender/eligibilityCriteria"]}),
    "R007": (
        "Unreasonable technical specifications",
        {
            "all": [
                "tender/documents/documentType",
                "tender/procurementMethod",
                "tender/items/classification/id",
                "tender/items/classification/scheme",
                BUYER_RULE,
                "tender/value/amount",
            ]
        },
    ),
    "R008": (
        "Unreasonable participation fees",
        {
            "all": [
                "tender/participationFees/value/amount",
                "tender/participationFees/value/currency",
                "tender/value/amount",
            ]
        },
    ),
    "R009": (
        "Buyer increases the cost of the bidding documents",
        {"all": ["tender/participationFees/value/amount", "tender/participationFees/value/currency", "date"]},
    ),
    "R010": (
        "Unjustified use of non competitive procedure",
        {"all": ["tender/procurementMethod", "tender/procurementMethodDetails", "tender/procurementMethodRationale"]},
    ),
    "R011": (
        "Splitting purchases to avoid procurement thresholds",
        {
            "all": [
                "tender/procurementMethod",
                ITEM_CLASSIFICATIONS_RULE,
                "tender/value/amount",
                "tender/value/currency",
                "tender/tenderPeriod/startDate",
                BUYER_RULE,
            ]
        },
    ),
    "R012": (
        "Direct awards in contravention of the provisions of the procurement plan",
        {"all": ["tender/procurementMethod", "tender/procurementMethodDetails", "planning/documents/documentType"]},
    ),
    "R013": ("High use of non competitive methods", {"all": ["tender/procurementMethod", BUYER_RULE]}),
    "R014": (
        "Short time between tender advertising and bid opening",
        {"all": ["tender/tenderPeriod/startDate", "tender/bidOpening/date", "tender/procurementMethod"]},
    ),
    "R015": (
        "Long time between bid opening and bid evaluation",
        {"all": ["tender/bidOpening/date", "tender/awardPeriod/startDate", "tender/procurementMethod"]},
    ),
    "R016": (
        "Tender value is higher or lower than average for this item category",
        {
            "all": [
                "tender/value/amount",
                "tender/value/currency",
                ITEM_CLASSIFICATIONS_RULE,
                "tender/procurementMethod",
            ]
        },
    ),
    "R017": ("Unreasonably low or high line item", {"all": [ITEM_CLASSIFICATIONS_RULE, UNIT_ITEMS_RULE]}),
    "R018": ("Single bid received", {"all": ["tender/procurementMethod", TENDERERS_COUNT_RULE]}),
    "R019": (
        "Low number of bidders for item and procuring entity",
        {"all": ["tender/procurementMethod", ITEM_CLASSIFICATIONS_RULE, BUYER_RULE, TENDERERS_COUNT_RULE]},
    ),
    "R020": ("Tender has a complaint", {"all": ["complaints/id"]}),
    "R021": ("High use of discretionary evaluation criteria", {"all": ["tender/awardCriteria", BUYER_RULE]}),
    "R022": (
        "Wide disparity in bid prices",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
            ]
        },
    ),
    "R023": (
        "Fixed multiple bid prices",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
            ]
        },
    ),
    "R024": (
        "Price close to winning bid",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                WINNING_BID_RULE,
            ]
        },
    ),
    "R025": (
        "Excessive unsuccessful bids",
        {"all": ["awards/suppliers/id", "bids/details/status", TENDERERS_RULE]},
    ),
    "R026": (
        "Prevalence of consortia",
        {
            "all": [
                "awards/suppliers/id",
                "awards/suppliers/name",
                "awards/status",
                "awards/date",
                ITEM_CLASSIFICATIONS_RULE,
            ]
        },
    ),
    "R027": (
        "Missing bidders",
        {"all": ["tender/procurementMethod", ITEM_CLASSIFICATIONS_RULE, TENDERERS_RULE, DATE_RULE]},
    ),
    "R028": (
        "Identical bid prices",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/tenderers/id",
            ]
        },
    ),
    "R029": ("Bid prices deviate from Benford's Law", {"all": [AMOUNT_RULE, ITEM_CLASSIFICATIONS_RULE]}),
    "R030": (
        "Late bid won",
        {
            "all": [
                "bids/details/id",
                "bids/details/date",
                "bids/details/status",
                "tender/tenderPeriod/endDate",
                WINNING_BID_RULE,
            ]
        },
    ),
    "R031": (
        "Winning bid price very close or higher than estimated price",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                "tender/value/amount",
                "tender/value/currency",
                WINNING_BID_RULE,
            ]
        },
    ),
    "R032": (
        "Bidders share same beneficial owner",
        {"all": ["parties/roles", "parties/id", "parties/beneficialOwners/name", "parties/beneficialOwners/id"]},
    ),
    "R033": (
        "Bidders share same major shareholder",
        {
            "all": [
                "parties/roles",
                "parties/id",
                "parties/shareholders/shareholder/id",
                "parties/shareholders/shareholding",
            ]
        },
    ),
    "R034": (
        "Bids submitted in same order",
        {
            "all": [
                "bids/details/id",
                "bids/details/date",
                "bids/details/tenderers/id",
                "bids/details/tenderers/name",
                "bids/details/status",
            ]
        },
    ),
    "R035": (
        "All except winning bid disqualified",
        {"all": ["bids/details/id", "bids/details/status", "awards/status", WINNING_BID_RULE]},
    ),
    "R036": (
        "Lowest bid disqualified",
        {
            "all": [
                "tender/awardCriteria",
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
            ]
        },
    ),
    "R037": (
        "Poorly supported disqualifications",
        {
            "all": [
                "tender/awardCriteria",
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                "bids/details/documents",
            ]
        },
    ),
    "R038": (
        "Excessive disqualified bids",
        {"all": ["bids/details/id", "bids/details/status", TENDERERS_RULE, BUYER_RULE]},
    ),
    "R039": (
        "Unanswered bidder questions",
        {
            "all": [
                "tender/enquiries/date",
                "tender/enquiries/dateAnswered",
                "tender/enquiries/answer",
                "tender/status",
            ]
        },
    ),
    "R040": (
        "High share of buyers contracts",
        {"all": [BUYER_RULE, "awards/status", "awards/date", "awards/suppliers/id", "awards/suppliers/name"]},
    ),
    "R041": (
        "Physical similarities in documents by different bidders",
        {"all": ["bids/details/id", "bids/details/tenderers/id", "bids/documents/documentType"]},
    ),
    "R042": ("Bidder has abnormal address or phone number", {"all": [BIDDERS_INFO_RULE]}),
    "R043": (
        "Bidder has same contact information as project official",
        {"all": ["parties/roles", "parties/id", CONTACT_INFO_RULE]},
    ),
    "R044": ("Business similarities between bidders", {"all": ["parties/roles", "parties/id", BIDDERS_INFO_RULE]}),
    "R045": ("Bidder is not listed in business registries", {"all": ["parties/roles", "parties/id"]}),
    "R046": ("Bidder is debarred or on sanctions list", {"all": ["parties/roles", "parties/id"]}),
    "R047": (
        "Supplier is not traceable on the web",
        {"all": ["awards/suppliers/name", "awards/suppliers/id", "parties/contactPoint/url"]},
    ),
    "R048": (
        "Heterogeneous supplier",
        {"all": [ITEM_CLASSIFICATIONS_RULE, "awards/suppliers/id", "awards/suppliers/name"]},
    ),
    "R049": (
        "Direct awards below threshold",
        {
            "all": [
                "awards/suppliers/id",
                "awards/suppliers/name",
                "awards/date",
                "tender/procurementMethod",
                BUYER_RULE,
            ]
        },
    ),
    "R050": (
        "High market share",
        {
            "all": [
                "awards/suppliers/id",
                "awards/suppliers/name",
                BUYER_RULE,
                "awards/value/amount",
                "awards/value/currency",
                ITEM_CLASSIFICATIONS_RULE,
                "awards/date",
                "awards/status",
            ]
        },
    ),
    "R051": (
        "High market concentration",
        {"all": ["awards/suppliers/id", "awards/suppliers/name", AWARDS_OR_CONTRACTS_RULE, ITEM_CLASSIFICATIONS_RULE]},
    ),
    "R052": (
        "Small initial purchase from supplier followed by much larger purchases",
        {
            "all": [
                "awards/suppliers/id",
                "awards/suppliers/name",
                "tender/procurementMethod",
                BUYER_RULE,
                AWARDS_OR_CONTRACTS_RULE,
            ]
        },
    ),
    "R053": (
        "Co-bidding pairs have same recurrent winner",
        {"all": ["bids/details/id", "bids/details/status", WINNING_BID_RULE]},
    ),
    "R054": (
        "Direct award followed by change orders that exceed the competitive threshold",
        {
            "all": [
                "tender/procurementMethod",
                "awards/value/amount",
                "awards/value/currency",
                "contracts/value/amount",
                "contracts/value/currency",
                "contracts/amendments/description",
            ]
        },
    ),
    "R055": (
        "Multiple direct awards above or just below competitive threshold",
        {
            "all": [
                "tender/procurementMethod",
                "awards/suppliers/id",
                "awards/suppliers/name",
                AWARDS_OR_CONTRACTS_RULE,
                BUYER_RULE,
            ]
        },
    ),
    "R056": (
        "Winning bid does not meet the award criteria",
        {"all": ["tender/awardCriteria", "bids/details/status", "bids/details/documents", WINNING_BID_RULE]},
    ),
    "R057": (
        "Bid rotation",
        {
            "all": [
                "bids/details/tenderers/id",
                "bids/details/tenderers/name",
                "awards/suppliers/id",
                "awards/suppliers/name",
                "bids/details/value/amount",
                "bids/details/value/currency",
                ITEM_CLASSIFICATIONS_RULE,
            ]
        },
    ),
    "R058": (
        "Heavily discounted bid",
        {
            "all": [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                WINNING_BID_RULE,
            ]
        },
    ),
    "R059": (
        "Large difference between the award value and final contract amount",
        {
            "all": [
                "awards/id",
                "awards/status",
                "awards/value/amount",
                "awards/value/currency",
                "contracts/awardID",
                "contracts/value/amount",
                "contracts/value/currency",
                "contracts/status",
            ]
        },
    ),
    "R060": (
        "Long time between award date and contract signature date",
        {"all": ["awards/date", "contracts/dateSigned", "tender/procurementMethod"]},
    ),
    "R061": (
        "Decision period extremely short",
        {"all": ["tender/tenderPeriod/endDate", "awards/date", "tender/procurementMethod"]},
    ),
    "R062": (
        "Decision period extremely long",
        {"all": ["tender/tenderPeriod/endDate", "awards/date", "tender/procurementMethod"]},
    ),
    "R063": ("Contract is not published", {"all": ["contracts/documents/documentType"]}),
    "R064": ("Contract has modifications", {"all": ["contracts/status", "contracts/amendments/description"]}),
    "R065": (
        "Contract amendments to reduce line items",
        {"all": ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"]},
    ),
    "R066": (
        "Contract amendments to increase line items",
        {"all": ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"]},
    ),
    "R067": (
        "Delivery failure",
        {
            "all": [
                "contracts/implementation/milestones/type",
                "contracts/implementation/milestones/dueDate",
                "contracts/implementation/milestones/dateMet",
            ]
        },
    ),
    "R068": (
        "Contract transactions exceed contract amount",
        {"all": ["contracts/value/amount", "contracts/value/currency", IMPLEMENTATION_VALUE_RULE]},
    ),
    "R069": (
        "Contract amendments to increase price",
        {"all": ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"]},
    ),
    "R070": (
        "Losing bidders are hired as subcontractors",
        {
            "all": [
                "contracts/relatedProcesses",
                "contracts/relatedProcesses/relationship",
                "awards/suppliers/id",
                TENDERERS_RULE,
            ]
        },
    ),
    "R071": (
        "A contractor subcontracts all or most of the work received",
        {"all": ["awards/hasSubcontracting", "awards/subcontracting/minimumPercentage"]},
    ),
    "R072": ("High prevalence of subcontracts", {"all": ["awards/hasSubcontracting", BUYER_RULE]}),
    "R073": (
        "Discrepancies between work completed and contract specifications",
        {
            "all": [
                "contracts/status",
                "contracts/documents/documentType",
                "contracts/implementation/documents/documentType",
            ]
        },
    ),
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


def redflags_checks(fields_list):
    """
    Return a table of the red flags checks.

    It indicates if the fields needed to calculate a particular indicator are present.
    """
    return pd.DataFrame(
        [
            {
                "red_flag": name,
                "R_id": r_id,
                "fields needed": ", ".join(_get_required_fields(rule)),
                "calculation": "possible to calculate" if _evaluate_rule(rule, fields_list) else "missing fields",
                "missing fields": ", ".join(_get_missing_fields(rule, fields_list)),
            }
            for r_id, (name, rule) in RED_FLAGS.items()
        ]
    )


def check_red_flags_indicators(result):
    # NEW Red Flags to OCDS mapping #Public
    spreadsheet_key = "1GACSPd64X5Tm-nu6LKttyEpaEp1CLsaCUGrEutljnFU"
    rows = authenticate_gspread().open_by_key(spreadsheet_key).get_worksheet(1).get_all_values()
    indicators = pd.DataFrame(rows).pipe(lambda df: df.rename(columns=df.iloc[0]).drop(df.index[0]))
    return result.merge(indicators.iloc[:, [0, 5, 6, 7]], on="R_id")


def get_coverage():
    """Calculate coverage for each red flag indicator using DSL rules."""
    return [
        pd.to_numeric(calculate_coverage(_get_required_fields(rule), "release_summary")["total_percentage"][0])
        for _name, rule in RED_FLAGS.values()
    ]


def most_common_fields_to_calculate_indicators(fields_table):
    """Count the most common fields used across all red flag indicators using DSL rules."""
    fields_count = (
        pd.DataFrame.from_dict(
            Counter(field for _name, rule in RED_FLAGS.values() for field in _get_required_fields(rule)),
            orient="index",
        )
        .reset_index()
        .rename(columns={"index": "field", 0: "number of indicators"})
        .sort_values("number of indicators", ascending=False)
        .reset_index(drop=True)
    )
    fields_count["published"] = np.where(fields_count["field"].isin(fields_table["path"]), "yes", "no")
    return fields_count
