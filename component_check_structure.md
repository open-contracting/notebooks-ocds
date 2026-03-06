## Check for structure and format errors

Kingfisher Collect reformats data sources as release packages or record packages. Check the `data_type` class attribute of the [spider](https://github.com/open-contracting/kingfisher-collect/tree/main/kingfisher_scrapy/spiders). If it is not 'release_package' or 'record_package', recommend to the publisher to package their data.

Kingfisher Process checks data against the OCDS schema using [lib-cove-ocds](https://github.com/open-contracting/lib-cove-ocds), same as the [OCDS Data Review Tool](https://review.standard.open-contracting.org). For release collections, Kingfisher Process stores check results in the `release_check` table. For record collections, Kingfisher Process stores check results in the `record_check` table.

### Confirm that checks are complete

If a crawl is scheduled using Kingfisher Collect, by default, Kingfisher Process performs structural checks. Checking data is the slowest step. For large collections, it is recommended to skip the `check` step or to collect only a sample. Otherwise, there can be a backlog of data to check.

Use this query to determine whether checks are complete for your collection(s).

If checks are in progress, you should wait for the checks to finish before running the queries in this section.

```sql
SELECT
    collection_id,
    'release' AS collection_type,
    CASE
        WHEN count(release.id) = count(release_check.id)
            THEN
                'complete'
        WHEN count(release_check.id) = 0
            THEN
                'not_started'
        ELSE
            'in_progress'
    END AS check_status,
    count(release_check.id)::text
    || '/'
    || count(release.id)::text AS check_progress
FROM
    release_check
RIGHT JOIN release ON release_check.release_id = release.id
WHERE
    collection_id IN :collection_ids
GROUP BY
    collection_id
UNION
SELECT
    collection_id,
    'record' AS collection_type,
    CASE
        WHEN count(record.id) = count(record_check.id)
            THEN
                'complete'
        WHEN count(record_check.id) = 0
            THEN
                'not_started'
        ELSE
            'in_progress'
    END AS check_status,
    count(record_check.id)::text
    || '/'
    || count(record.id)::text AS check_progress
FROM
    record_check
RIGHT JOIN record ON record_check.record_id = record.id
WHERE
    collection_id IN :collection_ids
GROUP BY
    collection_id;
```

### Error summary

Summarize the errors from the `release_check` and `record_check` tables.

```sql magic_args="structure_and_format_error_summary <<"
WITH errors AS (
    SELECT
        collection_id,
        errors ->> 'type' AS error_type,
        left(
            errors ->> 'description',
            49000
        ) AS error,
        ocid,
        errors ->> 'field' AS field,
        errors ->> 'value' AS value,
        row_number() OVER (
            PARTITION BY
                collection_id,
                errors ->> 'type',
                left(
                    errors ->> 'description',
                    49000
                )
        ) AS rownum
    FROM
        release_check AS rc
    CROSS JOIN
        jsonb_array_elements(cove_output -> 'validation_errors') AS errors
    INNER JOIN release AS r ON rc.release_id = r.id
    WHERE
        collection_id IN :collection_ids
    UNION ALL
    SELECT
        collection_id,
        errors ->> 'type' AS error_type,
        left(
            errors ->> 'description',
            49000
        ) AS error,
        ocid,
        errors ->> 'field' AS field,
        errors ->> 'value' AS value,
        row_number() OVER (
            PARTITION BY
                collection_id,
                errors ->> 'type',
                left(
                    errors ->> 'description',
                    49000
                )
        ) AS rownum
    FROM
        record_check AS rc
    CROSS JOIN
        jsonb_array_elements(cove_output -> 'validation_errors') AS errors
    INNER JOIN record AS r ON rc.record_id = r.id
    WHERE
        collection_id IN :collection_ids
),

examples AS (
    SELECT
        collection_id,
        error_type,
        field,
        error,
        array_agg(ocid) AS example_ocids,
        array_agg(value) AS example_values
    FROM
        errors
    WHERE
        rownum <= 3
    GROUP BY
        collection_id,
        error_type,
        field,
        error
)

SELECT
    collection_id,
    error_type,
    errors.field,
    error,
    count(*) AS count,
    example_ocids,
    example_values
FROM
    errors
INNER JOIN examples USING (collection_id, error_type, error)
GROUP BY
    collection_id,
    error_type,
    errors.field,
    error,
    example_ocids,
    example_values;
```

```python
structure_and_format_error_summary
```

### Error details

List all errors from the `release_check` and `record_check` tables.

```sql magic_args="structure_and_format_errors <<"
SELECT
    collection_id,
    'release' AS collection_type,
    errors ->> 'type' AS error_type,
    errors ->> 'field' AS field,
    left(
        errors ->> 'description',
        49000
    ) AS error,
    ocid,
    errors ->> 'value' AS value
FROM
    release_check AS rc
CROSS JOIN jsonb_array_elements(cove_output -> 'validation_errors') AS errors
INNER JOIN release AS r ON rc.release_id = r.id
WHERE
    collection_id IN :collection_ids
UNION ALL
SELECT
    collection_id,
    'record' AS collection_type,
    errors ->> 'type' AS error_type,
    errors ->> 'field' AS field,
    left(
        errors ->> 'description',
        49000
    ) AS error,
    ocid,
    errors ->> 'value' AS value
FROM
    record_check AS rc
CROSS JOIN jsonb_array_elements(cove_output -> 'validation_errors') AS errors
INNER JOIN record AS r ON rc.record_id = r.id
WHERE
    collection_id IN :collection_ids
```

```python
structure_and_format_errors
```

### Additional closed codelists

Using additional codes in the context of a closed codelist is an error

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
    additional_closed_codelist_values.value -> 'codelist' AS codelist,
    codes.value AS code,
    count(*) AS occurrences
FROM
    check_results
CROSS JOIN
    jsonb_each(
        results -> 'additional_closed_codelist_values'
    ) AS additional_closed_codelist_values
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
