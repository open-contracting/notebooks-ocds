import json
from collections import Counter
from functools import cache
from pathlib import Path

import jsonschema
import numpy as np
import pandas as pd
from ocdskingfishercolab import calculate_coverage


@cache
def _get_validator():
    """Load and cache the JSON schema validator."""
    schema_path = Path(__file__).parent / "indicators.schema.json"
    with schema_path.open() as f:
        schema = json.load(f)
    return jsonschema.Draft202012Validator(schema)


def _resolve_refs(rule, rules):
    """Recursively resolve $ref references in a rule."""
    if isinstance(rule, str):
        return rule
    if isinstance(rule, dict):
        if "$ref" in rule:
            ref_name = rule["$ref"]
            if ref_name not in rules:
                msg = f"Unknown rule reference: {ref_name}"
                raise ValueError(msg)
            return _resolve_refs(rules[ref_name], rules)
        return {key: _resolve_refs(value, rules) for key, value in rule.items()}
    if isinstance(rule, list):
        return [_resolve_refs(item, rules) for item in rule]
    return rule


def load_indicators(json_path=None, prefix=None):
    """
    Load indicators from JSON, resolve references, optionally filter by prefix.

    :param json_path: Path to the indicators JSON file. Defaults to indicators.json in the same directory.
    :param prefix: Optional prefix to filter indicators (e.g., "U" for usability, "R" for red flags).
    :returns: Dictionary mapping indicator IDs to (name, resolved_rule) tuples.
    :raises jsonschema.ValidationError: If the JSON does not conform to the schema.
    """
    json_path = Path(__file__).parent / "indicators.json" if json_path is None else Path(json_path)

    with json_path.open() as f:
        data = json.load(f)

    _get_validator().validate(data)

    rules = data.get("rules", {})
    return {
        id_: (ind["name"], _resolve_refs(ind["rule"], rules))
        for id_, ind in data["indicators"].items()
        if prefix is None or id_.startswith(prefix)
    }


def _find_best_any_option(options, field_list):
    """
    Find the option from an "any" rule with the fewest missing fields.

    Returns (best_option, missing_fields) tuple.
    """
    best_option = None
    best_missing = None

    for option in options:
        missing = _get_missing_fields(option, field_list)
        if not missing:
            return option, []
        if best_option is None or len(missing) < len(best_missing):
            best_option, best_missing = option, missing

    return best_option, best_missing


def _get_required_fields(rule, field_list):
    """
    Extract field names from a DSL rule for display purposes.

    For "any" rules, picks the option with the fewest missing fields.
    """
    if isinstance(rule, str):
        return [rule]
    if isinstance(rule, dict):
        if "all" in rule:
            fields = []
            for sub_rule in rule["all"]:
                fields.extend(_get_required_fields(sub_rule, field_list))
            return fields
        if "any" in rule:
            best_option, _ = _find_best_any_option(rule["any"], field_list)
            return _get_required_fields(best_option, field_list)
    return []


def _get_missing_fields(rule, field_list):
    """
    Get the missing fields for a DSL rule.

    For "any" rules, returns missing fields from the option with the fewest missing fields.
    """
    if isinstance(rule, str):
        return [] if rule in field_list else [rule]
    if isinstance(rule, dict):
        if "all" in rule:
            missing = []
            for sub_rule in rule["all"]:
                missing.extend(_get_missing_fields(sub_rule, field_list))
            return missing
        if "any" in rule:
            _, best_missing = _find_best_any_option(rule["any"], field_list)
            return best_missing
    return []


def indicator_checks(field_list, indicators):
    """
    Return a table of the indicator checks.

    It indicates if the fields needed to calculate a particular indicator are present.
    """
    return pd.DataFrame(
        [
            {
                "indicator": name,
                "id": indicator_id,
                "fields needed": ", ".join(_get_required_fields(rule, field_list)),
                "calculation": "possible to calculate"
                if not (missing := _get_missing_fields(rule, field_list))
                else "missing fields",
                "missing fields": ", ".join(missing),
            }
            for indicator_id, (name, rule) in indicators.items()
        ]
    )


def get_coverage(field_list, indicators):
    """Calculate coverage for each indicator using DSL rules."""
    return [
        pd.to_numeric(
            calculate_coverage(_get_required_fields(rule, field_list), "release_summary")["total_percentage"][0]
        )
        for _name, rule in indicators.values()
    ]


def most_common_fields_to_calculate_indicators(field_list, indicators):
    """Count the most common fields used across all indicators using DSL rules."""
    return (
        pd.DataFrame.from_dict(
            Counter(field for _name, rule in indicators.values() for field in _get_required_fields(rule, field_list)),
            orient="index",
        )
        .reset_index()
        .rename(columns={"index": "field", 0: "number of indicators"})
        .sort_values("number of indicators", ascending=False)
        .reset_index(drop=True)
        .assign(published=lambda df: np.where(df["field"].isin(field_list), "yes", "no"))
    )
