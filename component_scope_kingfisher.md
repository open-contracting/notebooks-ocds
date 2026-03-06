## Check scope

+++



Use this section to check:

* how many releases, records and compiled releases your data contains
* what stages of the contracting process your data covers
* what date range your data covers

If you are preparing an [Ad-hoc structure and format feedback](https://docs.google.com/document/d/1_k7eA2rI-k5EH8VESkVAB73wa_qrpplL-7dKgMLTGZc/edit#heading=h.i7tpu8c49dcv), you might skip this section.

+++

### Release and record counts

+++

Collections in Kingfisher Process contain either [releases](https://standard.open-contracting.org/latest/en/schema/reference/), [records](https://standard.open-contracting.org/latest/en/schema/records_reference/) or [compiled releases](https://standard.open-contracting.org/latest/en/schema/records_reference/#compiled-release). Kingfisher Process creates compiled release collections from release or record collections.

Use this section to check that the data contains the expected number of releases, records and compiled releases. Where possible, you should check these numbers against the total number of results available in the frontend of the data source.

Count the number of releases, records and compiled releases, for each collection.

**Note:** These columns are not yet populated in version 2 of Kingfisher Process. Comment on [this issue](https://github.com/open-contracting/kingfisher-process/issues/370) to prioritize it.

```{code-cell}
%%sql
SELECT
    id AS collection_id,
    cached_releases_count AS releases_count,
    cached_records_count AS records_count,
    cached_compiled_releases_count AS compiled_releases_count
FROM
    collection
WHERE
    id IN :collection_ids
```

### Contracting process stages

+++

Use this section to check that the data covers the expected stages of the contracting process.

+++

#### Release tags

+++

[Release tags](https://standard.open-contracting.org/latest/en/schema/codelists/#release-tag) indicate the stage of a contracting process to which a release is related.

+++

Count the number of releases, for each release tag:

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    tag,
    count(*)
FROM
    release_summary
GROUP BY
    collection_id,
    release_type,
    tag
ORDER BY
    collection_id
```

#### Objects per stage

+++

In OCDS, data is organized into objects, for each stage of a contracting process. Each compiled release has: at most one `Planning` object, at most one `Tender` object, any number of `Award` objects, and any number of `Contract` objects. Each `Contract` object has at most one `Implementation` object. As such, the number of `Award` objects can exceed the number of unique OCIDs, but the number of `Tender` objects can't.

+++

Plot a count of objects per stage:

```{code-cell}
%%sql objects_per_stage <<
SELECT
    CASE
        WHEN paths.path = 'contracts/implementation'
            THEN
                'implementation'
        ELSE
            paths.path
    END AS stage,
    CASE
        WHEN
            paths.path IN ('planning', 'tender', 'contracts/implementation')
            THEN
                greatest(field_counts.object_property, 0)
        ELSE
            greatest(field_counts.array_count, 0)
    END AS object_count
FROM (
    SELECT
        unnest(
            ARRAY[
                'planning',
                'tender',
                'awards',
                'contracts',
                'contracts/implementation'
            ]
        ) AS path
) AS paths
LEFT JOIN (
    SELECT *
    FROM
        field_counts
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
        AND path IN (
            'planning',
            'tender',
            'awards',
            'contracts',
            'contracts/implementation'
        )
) AS field_counts USING (path)
```

```{code-cell}
plot_objects_per_stage(objects_per_stage)
```

### Date ranges

+++


Use this section to check that the data covers the expected date range.

+++

Calculate the earliest and latest `date`, `awards/date` and `contracts/dateSigned`:

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    'release_date' AS date_type,
    min(date) AS min,
    max(date) AS max
FROM
    release_summary
GROUP BY
    collection_id,
    release_type,
    date_type
UNION ALL
SELECT
    collection_id,
    release_type,
    'award_date' AS date_type,
    min(first_award_date) AS min,
    max(last_award_date) AS max
FROM
    release_summary
GROUP BY
    collection_id,
    release_type,
    date_type
UNION ALL
SELECT
    collection_id,
    release_type,
    'contract_datesigned' AS date_type,
    min(first_contract_datesigned) AS min,
    max(last_contract_datesigned) AS max
FROM
    release_summary
GROUP BY
    collection_id,
    release_type
ORDER BY
    collection_id,
    release_type,
    date_type;
```

### Release date distribution

Use this section to check that releases are distributed as expected.

+++

Plot the count of releases per month:

```{code-cell}
%%sql release_dates <<
SELECT
    collection_id::text,
    release_type,
    date,
    count(*) AS release_count
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
GROUP BY
    collection_id,
    release_type,
    date
ORDER BY
    date ASC;
```

```{code-cell}
# Resample by month
release_dates["date"] = release_dates["date"].dt.strftime("%Y-%m")
release_dates = (
    release_dates.groupby(["collection_id", "release_type", "date"]).agg({"release_count": "sum"}).reset_index()
)

plot_releases_by_month(release_dates)
```

### Extensions

+++

Use this section to check which extensions the data uses.

+++

List the extensions declared in the package metadata:

```{code-cell}
%%sql
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
