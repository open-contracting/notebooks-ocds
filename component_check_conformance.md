## Perform manual conformance checks

[Conforming publications](https://standard.open-contracting.org/latest/en/schema/conformance_and_extensions/#publication-conformance):

* Use a [registered OCID prefix](https://standard.open-contracting.org/latest/en/schema/identifiers/#contracting-process-identifier-ocid).
* The [OCDS Data Review Tool](https://standard.open-contracting.org/review/) can report results on the data.
* Must not use terms from outside the OCDS schema where its terms would suffice.

Use this section to:

* Check if the proper OCID prefix is in use.
* Check if the OCDS Data Review Tool is able to report results on data.
* Identify fields in local extensions and additional fields and codes that should be mapped to fields and codes in the OCDS schema and extensions.
* Identify deprecated fields, in order to recommend a change to the publisher's OCDS implementation.

You can use the following resources to find fields and codes with similar semantics:

* [OCDS Schema and Codelist Reference](https://standard.open-contracting.org/latest/en/schema/), for fields in the core OCDS schema.
* [OCDS Extensions Field and Code Search](https://open-contracting.github.io/editor-tools/), for fields and codes in OCDS extensions.
* [GitHub Issue Tracker](https://github.com/open-contracting/standard/issues), for discussions about adding new fields and codes.

Check that field and code names [conform to the style guide](https://ocds-standard-development-handbook.readthedocs.io/en/latest/meta/schema_style_guide.html#field-and-code-names) and report any issues to the publisher.

If you cannot find a suitable mapping for an additional field or code, [open a GitHub issue](https://github.com/open-contracting/standard/issues) to describe the semantics of the field or code and to discuss how to model it. Report any issues to the publisher.

**Note:** This section depends on the `check` step of Kingfisher Process having completed. See *Check for structure and format errors >Confirm that checks are complete*. If the checks are not complete or the OCDS Data Review Tool is not able to report results on data, **the publisher don't pass that conformance criterion**

### OCID prefix

Check that the data uses the OCID prefix that was issued to this specific publisher.

You only need to run either the *Release prefixes* or *Record prefixes* section, depending on the publication's data format.

Update the ocid prefix in the appropriate cell. Prefixes can be found at [the list of registered prefixes](https://docs.google.com/spreadsheets/d/1E5ZVhc8VhGOakCq4GegvkyFYT974QQb-sSjvOfaxH7s/pubhtml?gid=506986894&single=true&widget=true).

#### **Release prefixes**

Notify the publisher of any incorrect prefixes.

```python
# Do not remove the final % character
ocid_prefix = "%"
```

```sql magic_args="ocid_prefix_release_check <<"
SELECT ocid
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND ocid NOT LIKE :ocid_prefix
```

```python
ocid_prefix_release_check
```

#### **Record prefixes**

Notify the publisher of any incorrect prefixes.

```sql magic_args="ocid_prefix_record_check <<"
SELECT ocid
FROM
    record_summary
WHERE
    collection_id IN :collection_ids
    AND ocid NOT LIKE :ocid_prefix
```

```python
ocid_prefix_record_check
```

### Local extensions

For each field and code in extensions authored by the publisher, in addition to the above checks, consider whether to [review the extension in detail](https://docs.google.com/document/d/1CS_TMubqoYaucT8JXPTgLS-mF4eMIifX-6mD0xpWg9M/edit).

List the extensions declared in the package metadata.

**Note:** This query should be kept in sync with the query in *Check scope > Extensions*.

```sql
SELECT
    collection_id,
    release_type,
    jsonb_array_elements(package_data -> 'extensions') AS ocds_extension,
    count(*) AS count
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND package_data IS NOT NULL
GROUP BY
    collection_id,
    release_type,
    ocds_extension
ORDER BY
    collection_id ASC,
    release_type ASC,
    count DESC;
```

### Additional fields

[lib-cove-ocds](https://github.com/open-contracting/lib-cove-ocds) reports additional fields in the following scenarios:

* Fields from undeclared extensions.
* Fields with language variations, e.g. `title_es`. You do not need to report language variations to the publisher, but you should check that the field [conforms to the rules for language variations](https://standard.open-contracting.org/latest/en/schema/reference/#language).
* OCDS 1.0 data using extension fields. You should report the fields to the publisher and recommend that they upgrade to OCDS 1.1.

List additional fields.

By default, results are reported for a sample of 10% of releases. For small collections, you can set `sample_size` to `1` to return results for the full collection. For large collections, you can reduce the sample size.

```python
sample_size = 0.1
```

```sql
WITH check_results AS (
    SELECT
        *,
        CASE
            WHEN (release_type IN ('record', 'embedded_release'))
                THEN
                    record_check
            ELSE
                release_check
        END AS results
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type <> 'compiled_release'
        AND random() < :sample_size
),

counts AS (
    SELECT
        collection_id,
        release_type,
        additional_fields ->> 'path' AS path,
        additional_fields ->> 'field_name' AS field,
        sum((additional_fields ->> 'count')::int) AS count
    FROM
        check_results
    CROSS JOIN
        jsonb_array_elements(
            results -> 'all_additional_fields'
        ) AS additional_fields
    GROUP BY
        collection_id,
        release_type,
        field,
        path
    ORDER BY
        path ASC,
        count DESC
),

examples AS (
    SELECT DISTINCT ON (
        collection_id,
        release_type,
        additional_fields ->> 'path',
        additional_fields ->> 'field_name')
        collection_id,
        release_type,
        additional_fields ->> 'path' AS path,
        additional_fields ->> 'field_name' AS field,
        additional_fields ->> 'examples' AS examples
    FROM
        check_results
    CROSS JOIN
        jsonb_array_elements(
            results -> 'all_additional_fields'
        ) AS additional_fields
    WHERE
        jsonb_array_length(additional_fields -> 'examples') > 0
)

SELECT
    counts.collection_id,
    counts.release_type,
    counts.path,
    counts.field,
    count,
    examples
FROM
    counts
LEFT JOIN examples
    USING (
        collection_id,
        release_type,
        path,
        field
    )
ORDER BY
    path,
    field;
```

#### Additional field examples

Generate a release package containing an example release for each additional field:

```sql magic_args="additional_field_examples <<"
WITH additional_field_releases AS (
    SELECT
        ocid,
        release.release_id,
        data_id,
        additional_fields ->> 'path' AS path,
        additional_fields ->> 'field_name' AS field
    FROM
        release_check
    CROSS JOIN
        jsonb_array_elements(
            cove_output -> 'all_additional_fields'
        ) AS additional_fields
    INNER JOIN release ON release_check.release_id = release.id
    WHERE
        collection_id IN :collection_ids
        AND random() < :sample_size
),

additional_fields AS (
    SELECT DISTINCT
        path,
        field
    FROM
        additional_field_releases
),

examples AS (
    SELECT DISTINCT ON (
        additional_fields.path,
        additional_fields.field)
        additional_fields.path,
        additional_fields.field,
        ocid,
        release_id,
        data_id,
        data
    FROM
        additional_fields
    INNER JOIN additional_field_releases
        ON
            additional_fields.path = additional_field_releases.path
            AND additional_fields.field = additional_field_releases.field
    INNER JOIN data ON data.id = data_id
    ORDER BY
        additional_fields.path,
        additional_fields.field
)

SELECT jsonb_build_object('releases', jsonb_agg(data)) AS release_package
FROM
    examples
```

```python
render_json(additional_field_examples["release_package"][0])
```

### Additional open codes

List additional codes in the context of an open codelist.

Using additional codes in the context of a closed codelist is an error, and is reported in the *Check for structure and format errors* section.

```sql
WITH check_results AS (
    SELECT
        *,
        CASE
            WHEN (release_type IN ('record', 'embedded_release'))
                THEN
                    record_check
            ELSE
                release_check
        END AS results
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type <> 'compiled_release'
)

SELECT
    collection_id,
    release_type,
    additional_open_codelist_values.value -> 'codelist' AS codelist,
    codes.value AS code,
    count(*) AS occurrences
FROM
    check_results
CROSS JOIN
    jsonb_each(
        results -> 'additional_open_codelist_values'
    ) AS additional_open_codelist_values
CROSS JOIN jsonb_array_elements(value -> 'values') AS codes
GROUP BY
    collection_id,
    release_type,
    codelist,
    code
ORDER BY
    collection_id,
    release_type,
    codelist,
    count(*) DESC
```

### Deprecated fields

Before a field or codelist is removed from the standard, it is first marked as [deprecated](https://standard.open-contracting.org/latest/en/governance/deprecation/#deprecation).

Use this section to check for deprecated fields.

List deprecated fields:

```sql
SELECT DISTINCT ON (collection_id, path, deprecated_version, explanation)
    collection_id,
    regexp_replace(trim('"' FROM paths::text), '\/[0-9]+', '', 'g')
    || '/'
    || (deprecated_fields ->> 'field') AS path,
    deprecated_fields -> 'explanation' -> 0 AS deprecated_version,
    deprecated_fields -> 'explanation' -> 1 AS explanation,
    ocid AS example_ocid
FROM
    release_check
CROSS JOIN
    jsonb_array_elements(
        cove_output -> 'deprecated_fields'
    ) AS deprecated_fields
CROSS JOIN jsonb_array_elements(deprecated_fields -> 'paths') AS paths
INNER JOIN release ON release_check.release_id = release.id
WHERE
    collection_id IN :collection_ids;
```
