# ## Red flags analysis setup
#
# Use this section to setup the functions needed to perform a usability analysis of the dataset, to identify if a publisher has the necessary fields to calculate 73 red flags indicators.

# +
# @title Red flags functions { display-mode: "form" }
def check_red_flags_indicators(result):
    gc = authenticate_gspread()

    # NEW Red Flags to OCDS mapping #Public
    worksheet = gc.open_by_key("1GACSPd64X5Tm-nu6LKttyEpaEp1CLsaCUGrEutljnFU").get_worksheet(1)

    # get_all_values gives a list of rows.
    rows = worksheet.get_all_values()
    # Convert to a DataFrame and render.

    indicators = pd.DataFrame(rows)
    indicators = indicators.rename(columns=indicators.iloc[0]).drop(indicators.index[0])
    indicatorsdf = indicators.iloc[:, [0, 5, 6, 7]]

    return result.merge(indicatorsdf, on="R_id")


def most_common_fields_to_calculate_indicators(indicators_dict, fields_table):
    fields = list(indicators_dict.values())
    fields = [item[1:] for item in fields]
    flat_list = [item for sublist in [item for sublist in fields for item in sublist] for item in sublist]
    fields_list = Counter(flat_list)

    fields_count = (
        pd.DataFrame.from_dict(fields_list, orient="index")
        .reset_index()
        .rename(columns={"index": "field", 0: "number of indicators"})
    )

    fields_count = fields_count.sort_values("number of indicators", ascending=False).reset_index(drop=True)
    fields_count["published"] = np.where(fields_count["field"].isin(fields_table["path"]), "yes", "no")

    return fields_count


def get_coverage(indicators_dic):
    coverage = []
    for i in indicators_dic.values():
        fields = [item for sublist in i for item in sublist][1:]
        result = calculate_coverage(fields, "release_summary")
        result_value = pd.to_numeric(result["total_percentage"][0])
        coverage.append(result_value)
    return coverage


def get_red_flags_dictionary(fields_list):
    """To calculate some indicators there are alternative fields that can be used, for example to calculate the number of tenderers  both the `tender/numberOfTenderers` or the `tender/tenderers/id` could be used.  This section checks which fields are available in the publication."""
    # buyers
    buyer = ["buyer/name", "buyer/id"]
    procuring = ["tender/procuringEntity/name", "tender/procuringEntity/id"]
    parties = ["parties/name", "parties/id", "parties/roles"]
    if not any(item not in fields_list for item in buyer):
        buyer_var = buyer
    elif not any(item not in fields_list for item in procuring):
        buyer_var = procuring
    elif not any(item not in fields_list for item in parties):
        buyer_var = parties
    else:
        buyer_var = buyer

    # bidders
    if "tender/tenderers/id" in fields_list:
        bidders_val = "tender/tenderers/id"
    elif "bids/details/tenderers/id" in fields_list:
        bidders_val = "bids/details/tenderers/id"
    else:
        bidders_val = "tender/tenderers/id"

    # number of tendereres
    if "tender/numberOfTenderers" in fields_list:
        bidders_val2 = "tender/numberOfTenderers"
    elif "tender/tenderers/id" in fields_list:
        bidders_val2 = "tender/tenderers/id"
    elif "bids/details/tenderers/id" in fields_list:
        bidders_val2 = "bids/details/tenderers/id"
    elif "bids/statistics/value" in fields_list:
        bidders_val2 = "bids/statistics/value"
    else:
        bidders_val2 = "tender/numberOfTenderers"

    # suppliers
    parties = ["parties/id", "parties/roles"]

    bidders_val = "bids/details/tenderers/id" if "bids/details/tenderers/id" in fields_list else "tender/tenderers/id"

    # awards and contracts fields
    aw = ["awards/status", "awards/date", "awards/value/amount", "awards/value/currency"]
    con = ["contracts/status", "contracts/dateSigned", "contracts/value/amount", "contracts/value/currency"]
    if not any(item not in fields_list for item in aw):
        awards_val3 = aw
    elif not any(item not in fields_list for item in con):
        awards_val3 = con
    else:
        awards_val3 = aw

    # items
    tender_it = ["tender/items/classification/id", "tender/items/classification/scheme"]
    awards_it = ["awards/items/classification/id", "awards/items/classification/scheme"]
    contracts_it = ["contracts/items/classification/id", "contracts/items/classification/scheme"]
    if not any(item not in fields_list for item in tender_it):
        item_var = tender_it
    elif not any(item not in fields_list for item in awards_it):
        item_var = awards_it
    elif not any(item not in fields_list for item in contracts_it):
        item_var = contracts_it
    else:
        item_var = tender_it

    # unit items
    unit_tender_it = ["tender/items/unit/value/amount", "tender/items/unit/value/currency"]
    unit_awards_it = ["awards/items/unit/value/amount", "awards/items/unit/value/amount"]
    unit_contracts_it = ["contracts/items/unit/value/amount", "contracts/items/unit/value/amount"]
    if not any(item not in fields_list for item in unit_tender_it):
        unit_item_var = unit_tender_it
    elif not any(item not in fields_list for item in unit_awards_it):
        unit_item_var = unit_awards_it
    elif not any(item not in fields_list for item in unit_contracts_it):
        unit_item_var = unit_contracts_it
    else:
        unit_item_var = unit_tender_it

    # date fields
    if "tender/tenderPeriod/startDate" in fields_list:
        date_var = "tender/tenderPeriod/startDate"
    elif "awards/date" in fields_list:
        date_var = "awards/date"
    else:
        date_var = "tender/tenderPeriod/startDate"

    # amounts fields
    if "tender/value/amount" in fields_list:
        amount_var = "tender/value/amount"
    elif "bids/details/value/amount" in fields_list:
        amount_var = "bids/details/value/amount"
    elif "awards/value/amount" in fields_list:
        amount_var = "awards/value/amount"
    elif "contracts/value/amount" in fields_list:
        amount_var = "contracts/value/amount"
    else:
        amount_var = "bids/details/value/amount"

    # winning bids
    win_bid = ["bids/awards/relatedBid"]
    win_bid2 = ["bids/details/tenderers/id", "awards/suppliers/id"]
    if not any(item not in fields_list for item in win_bid):
        win_bid_var = win_bid
    elif not any(item not in fields_list for item in win_bid2):
        win_bid_var = win_bid2
    else:
        win_bid_var = win_bid

    # bidder info
    if "parties/contactPoint/telephone" in fields_list:
        bidders_info_var = "parties/contactPoint/telephone"
    elif "parties/address/streetAddress" in fields_list:
        bidders_info_var = "parties/address/streetAddress"
    elif "parties/address/postalCode" in fields_list:
        bidders_info_var = "parties/address/postalCode"
    else:
        bidders_info_var = "parties/contactPoint/telephone"

    # contact info
    if "parties/contactPoint/telephone" in fields_list:
        contact_info_var = "parties/contactPoint/telephone"
    elif "parties/contactPoint/email" in fields_list:
        contact_info_var = "parties/contactPoint/email"
    elif "parties/contactPoint/name" in fields_list:
        contact_info_var = "parties/contactPoint/name"
    else:
        contact_info_var = "parties/contactPoint/telephone"

    # implementation values
    imp_val = ["contracts/implementation/finalValue/amount", "contracts/implementation/finalValue/currency"]
    imp_val2 = [
        "contracts/implementation/transactions/value/amount",
        "contracts/implementation/transactions/value/currency",
    ]
    if not any(item not in fields_list for item in imp_val):
        imp_val_var = imp_val
    elif not any(item not in fields_list for item in imp_val2):
        imp_val_var = imp_val2
    else:
        imp_val_var = imp_val

    return {
        "Planning documents not available": [["R001"], ["planning/documents/documentType"]],
        "Manipulation of procurement thresholds": [
            ["R002"],
            [
                "tender/value/amount",
                "tender/value/currency",
                "tender/procurementMethod",
                "tender/tenderPeriod/startDate",
                *buyer_var,
            ],
        ],
        " The submission period is too short": [
            ["R003"],
            ["tender/tenderPeriod/startDate", "tender/tenderPeriod/endDate", "tender/procurementMethod"],
        ],
        "Failure to adequately advertise the request for bids": [
            ["R004"],
            ["tender/documents/documentType", "tender/documents/datePublished", "tender/tenderPeriod/startDate"],
        ],
        "Key tender information and documents are not available": [
            ["R005"],
            [
                "tender/documents/documentType",
                "tender/documents/datePublished",
                "tender/tenderPeriod/startDate",
                "tender/tenderPeriod/endDate",
            ],
        ],
        "Unreasonable prequalification requirements": [["R006"], ["tender/eligibilityCriteria"]],
        "Unreasonable technical specifications": [
            ["R007"],
            [
                "tender/documents/documentType",
                "tender/procurementMethod",
                "tender/items/classification/id",
                "tender/items/classification/scheme",
                *buyer_var,
                "tender/value/amount",
            ],
        ],
        "Unreasonable participation fees": [
            ["R008"],
            [
                "tender/participationFees/value/amount",
                "tender/participationFees/value/currency",
                "tender/value/amount",
            ],
        ],
        "Buyer increases the cost of the bidding documents": [
            ["R009"],
            ["tender/participationFees/value/amount", "tender/participationFees/value/currency", "date"],
        ],
        "Unjustified use of non competitive procedure": [
            ["R010"],
            ["tender/procurementMethod", "tender/procurementMethodDetails", "tender/procurementMethodRationale"],
        ],
        "Splitting purchases to avoid procurement thresholds": [
            ["R011"],
            [
                "tender/procurementMethod",
                *item_var,
                "tender/value/amount",
                "tender/value/currency",
                "tender/tenderPeriod/startDate",
                *buyer_var,
            ],
        ],
        "Direct awards in contravention of the provisions of the procurement plan": [
            ["R012"],
            ["tender/procurementMethod", "tender/procurementMethodDetails", "planning/documents/documentType"],
        ],
        "High use of non competitive methods": [["R013"], ["tender/procurementMethod", *buyer_var]],
        "Short time between tender advertising and bid opening": [
            ["R014"],
            ["tender/tenderPeriod/startDate", "tender/bidOpening/date", "tender/procurementMethod"],
        ],
        "Long time between bid opening and bid evaluation": [
            ["R015"],
            ["tender/bidOpening/date", "tender/awardPeriod/startDate", "tender/procurementMethod"],
        ],
        "Tender value is higher or lower than average for this item category": [
            ["R016"],
            ["tender/value/amount", "tender/value/currency", *item_var, "tender/procurementMethod"],
        ],
        "Unreasonably low or high line item": [["R017"], [*item_var, *unit_item_var]],
        "Single bid received": [["R018"], ["tender/procurementMethod", bidders_val2]],
        "Low number of bidders for item and procuring entity": [
            ["R019"],
            ["tender/procurementMethod", *item_var, *buyer_var, bidders_val2],
        ],
        "Tender has a complaint": [["R020"], ["complaints/id"]],
        "High use of discretionary evaluation criteria": [["R021"], ["tender/awardCriteria", *buyer_var]],
        "Wide disparity in bid prices": [
            ["R022"],
            ["bids/details/id", "bids/details/value/amount", "bids/details/value/currency", "bids/details/status"],
        ],
        "Fixed multiple bid prices": [
            ["R023"],
            ["bids/details/id", "bids/details/value/amount", "bids/details/value/currency", "bids/details/status"],
        ],
        "Price close to winning bid": [
            ["R024"],
            [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                *win_bid_var,
            ],
        ],
        "Excessive unsuccessful bids": [["R025"], ["awards/suppliers/id", "bids/details/status", bidders_val]],
        "Prevalence of consortia": [
            ["R026"],
            ["awards/suppliers/id", "awards/suppliers/name", "awards/status", "awards/date", *item_var],
        ],
        "Missing bidders": [["R027"], ["tender/procurementMethod", *item_var, bidders_val, date_var]],
        "Identical bid prices": [
            ["R028"],
            [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/tenderers/id",
            ],
        ],
        "Bid prices deviate from Benford's Law": [["R029"], [amount_var, *item_var]],
        "Late bid won": [
            ["R030"],
            [
                "bids/details/id",
                "bids/details/date",
                "bids/details/status",
                "tender/tenderPeriod/endDate",
                *win_bid_var,
            ],
        ],
        "Winning bid price very close or higher than estimated price": [
            ["R031"],
            [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                "tender/value/amount",
                "tender/value/currency",
                *win_bid_var,
            ],
        ],
        "Bidders share same beneficial owner": [
            ["R032"],
            ["parties/roles", "parties/id", "parties/beneficialOwners/name", "parties/beneficialOwners/id"],
        ],
        "Bidders share same major shareholder": [
            ["R033"],
            [
                "parties/roles",
                "parties/id",
                "parties/shareholders/shareholder/id",
                "parties/shareholders/shareholding",
            ],
        ],
        " Bids submitted in same order": [
            ["R034"],
            [
                "bids/details/id",
                "bids/details/date",
                "bids/details/tenderers/id",
                "bids/details/tenderers/name",
                "bids/details/status",
            ],
        ],
        "All except winning bid disqualified": [
            ["R035"],
            ["bids/details/id", "bids/details/status", "awards/status", *win_bid_var],
        ],
        "Lowest bid disqualified ": [
            ["R036"],
            [
                "tender/awardCriteria",
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
            ],
        ],
        "Poorly supported disqualifications": [
            ["R037"],
            [
                "tender/awardCriteria",
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                "bids/details/documents",
            ],
        ],
        "Excessive disqualified bids": [["R038"], ["bids/details/id", "bids/details/status", bidders_val, *buyer_var]],
        "Unanswered bidder questions": [
            ["R039"],
            ["tender/enquiries/date", "tender/enquiries/dateAnswered", "tender/enquiries/answer", "tender/status"],
        ],
        "High share of buyers contracts": [
            ["R040"],
            [*buyer_var, "awards/status", "awards/date", "awards/suppliers/id", "awards/suppliers/name"],
        ],
        "Physical similarities in documents by different bidders": [
            ["R041"],
            ["bids/details/id", "bids/details/tenderers/id", "bids/documents/documentType"],
        ],
        "Bidder has abnormal address or phone number": [["R042"], [bidders_info_var]],
        "Bidder has same contact information as project official": [
            ["R043"],
            ["parties/roles", "parties/id", contact_info_var],
        ],
        "Business similarities between bidders": [["R044"], ["parties/roles", "parties/id", bidders_info_var]],
        "Bidder is not listed in  business registries": [["R045"], ["parties/roles", "parties/id"]],
        "Bidder is debarred or on sanctions list": [["R046"], ["parties/roles", "parties/id"]],
        "Supplier is not traceable on the web": [
            ["R047"],
            ["awards/suppliers/name", "awards/suppliers/id", "parties/contactPoint/url"],
        ],
        "Heterogeneous supplier": [["R048"], [*item_var, "awards/suppliers/id", "awards/suppliers/name"]],
        "Direct awards below threshold": [
            ["R049"],
            ["awards/suppliers/id", "awards/suppliers/name", "awards/date", "tender/procurementMethod", *buyer_var],
        ],
        " High market share": [
            ["R050"],
            [
                "awards/suppliers/id",
                "awards/suppliers/name",
                *buyer_var,
                "awards/value/amount",
                "awards/value/currency",
                *item_var,
                "awards/date",
                "awards/status",
            ],
        ],
        "High market concentration": [
            ["R051"],
            ["awards/suppliers/id", "awards/suppliers/name", *awards_val3, *item_var],
        ],
        "Small initial purchase from supplier followed by much larger purchases": [
            ["R052"],
            ["awards/suppliers/id", "awards/suppliers/name", "tender/procurementMethod", *buyer_var, *awards_val3],
        ],
        "Co-bidding pairs have same recurrent winner": [
            ["R053"],
            ["bids/details/id", "bids/details/status", *win_bid_var],
        ],
        "Direct award followed by change orders  that exceed the competitive threshold": [
            ["R054"],
            [
                "tender/procurementMethod",
                "awards/value/amount",
                "awards/value/currency",
                "contracts/value/amount",
                "contracts/value/currency",
                "contracts/amendments/description",
            ],
        ],
        "Multiple direct awards above or just below competitive threshold": [
            ["R055"],
            ["tender/procurementMethod", "awards/suppliers/id", "awards/suppliers/name", *awards_val3, *buyer_var],
        ],
        "Winning bid does not meet the award criteria": [
            ["R056"],
            ["tender/awardCriteria", "bids/details/status", "bids/details/documents", *win_bid_var],
        ],
        " Bid rotation": [
            ["R057"],
            [
                "bids/details/tenderers/id",
                "bids/details/tenderers/name",
                "awards/suppliers/id",
                "awards/suppliers/name",
                "bids/details/value/amount",
                "bids/details/value/currency",
                *item_var,
            ],
        ],
        "Heavily discounted bid": [
            ["R058"],
            [
                "bids/details/id",
                "bids/details/value/amount",
                "bids/details/value/currency",
                "bids/details/status",
                *win_bid_var,
            ],
        ],
        "Large difference between the award value and final contract amount": [
            ["R059"],
            [
                "awards/id",
                "awards/status",
                "awards/value/amount",
                "awards/value/currency",
                "contracts/awardID",
                "contracts/value/amount",
                "contracts/value/currency",
                "contracts/status",
            ],
        ],
        "Long time between award date and contract signature date": [
            ["R060"],
            ["awards/date", "contracts/dateSigned", "tender/procurementMethod"],
        ],
        "Decision period extremely short": [
            ["R061"],
            ["tender/tenderPeriod/endDate", "awards/date", "tender/procurementMethod"],
        ],
        "Decision period extremely long": [
            ["R062"],
            ["tender/tenderPeriod/endDate", "awards/date", "tender/procurementMethod"],
        ],
        "Contract is not published": [["R063"], ["contracts/documents/documentType"]],
        "Contract has modifications": [["R064"], ["contracts/status", "contracts/amendments/description"]],
        "Contract amendments to reduce line items": [
            ["R065"],
            ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"],
        ],
        "Contract amendments to increase line items": [
            ["R066"],
            ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"],
        ],
        "Delivery failure": [
            ["R067"],
            [
                "contracts/implementation/milestones/type",
                "contracts/implementation/milestones/dueDate",
                "contracts/implementation/milestones/dateMet",
            ],
        ],
        "Contract transactions exceed contract amount": [
            ["R068"],
            ["contracts/value/amount", "contracts/value/currency", *imp_val_var],
        ],
        "Contract amendments to increase price": [
            ["R069"],
            ["contracts/status", "contracts/amendments/description", "contracts/amendments/rationale"],
        ],
        "Losing bidders are hired as subcontractors": [
            ["R070"],
            [
                "contracts/relatedProcesses",
                "contracts/relatedProcesses/relationship",
                "awards/suppliers/id",
                bidders_val,
            ],
        ],
        "A contractor subcontracts all or most of the work received": [
            ["R071"],
            ["awards/hasSubcontracting", "awards/subcontracting/minimumPercentage"],
        ],
        "High prevalence of subcontracts": [["R072"], ["awards/hasSubcontracting", *buyer_var]],
        "Discrepancies between work completed and contract specifications": [
            ["R073"],
            [
                "contracts/status",
                "contracts/documents/documentType",
                "contracts/implementation/documents/documentType",
            ],
        ],
    }


def redflags_checks(fields_list, indicators_dic, *, check_coverage=False):
    """
    Return a table of the usability checks.

    It indicates if the fields needed to calculate a particular indicator are present.
    Set check_coverage=True to check for coverage
    """
    results_list = []
    missing_fields = []

    for i in indicators_dic.values():
        check = any(item not in fields_list for item in i[1])
        result = "missing fields" if check else "possible to calculate"
        missing = [i[1][j] for j in range(len(i[1])) if i[1][j] not in fields_list]
        missing_fields.append(missing)
        results_list.append(result)

    # Generate dataframe

    indicatordf = pd.DataFrame(
        list(
            zip(
                list(indicators_dic),
                [indicators_dic[i][0] for i in indicators_dic],
                [indicators_dic[i][1:] for i in indicators_dic],
                strict=True,
            )
        ),
        columns=["red_flag", "R_id", "fields needed"],
    )
    indicatordf["R_id"] = indicatordf["R_id"].apply(lambda x: ", ".join(map(str, x)))
    indicatordf["fields needed"] = indicatordf["fields needed"].astype(str).str.replace(r"\[|\]|'", "", regex=True)
    indicatordf["calculation"] = results_list
    indicatordf["missing fields"] = missing_fields
    indicatordf["missing fields"] = indicatordf["missing fields"].apply(lambda x: ", ".join(map(str, x)))

    if check_coverage:
        # Calculate coverage
        coverage = []
        for i in indicators_dic.values():
            fields = [item for sublist in i for item in sublist][1:]
            result = calculate_coverage(fields, "release_summary")
            result_value = pd.to_numeric(result["total_percentage"][0])
            coverage.append(result_value)
        indicatordf["coverage"] = coverage
    return indicatordf
