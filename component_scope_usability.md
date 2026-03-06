## Calculate general statistics

+++

Use this section to have an overview of the dataset in terms of fields published, stages covered and key summary statistics.  You can add any additional queries as needed.

+++

###Fields published

+++

Calculate the fields published

```{code-cell}
%%sql fields_table <<
SELECT
    path,
    distinct_releases
FROM
    field_counts
WHERE
    release_type = 'compiled_release'
```

```{code-cell}
fields_table
```

Save fields table in spreadsheet:

```{code-cell}
spreadsheet_name = input("Enter the name of your spreadsheet:")
save_dataframe_to_sheet(spreadsheet_name, fields_table, "fields")
```

### Stages covered

```{code-cell}
%%sql stages <<
WITH field_counts AS (
    SELECT *
    FROM
        field_counts
    WHERE
        release_type = 'compiled_release'
        AND path IN (
            'planning',
            'tender',
            'awards',
            'contracts',
            'contracts/implementation'
        )
)

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
LEFT JOIN field_counts USING (path)
```

```{code-cell}
stages
```

```{code-cell}
plot_objects_per_stage(stages)
```

### Number of tenders and awards by date

```{code-cell}
%%sql dates <<
WITH tenders AS (
    SELECT
        extract(YEAR FROM tenderperiod_startdate) AS year,
        count(*) AS tenders
    FROM
        tender_summary
    WHERE
        release_type = 'compiled_release'
        AND tenderperiod_startdate IS NOT NULL
    GROUP BY
        year
    ORDER BY
        year
),

awards AS (
    SELECT
        extract(YEAR FROM date) AS year,
        count(*) AS awards
    FROM
        awards_summary
    WHERE
        release_type = 'compiled_release'
        AND date IS NOT NULL
    GROUP BY
        year
    ORDER BY
        year
)

SELECT
    t.year::integer,
    tenders,
    awards
FROM
    tenders AS t
FULL JOIN awards AS a ON t.year = a.year
```

```{code-cell}
dates
```

```{code-cell}
plot_objects_per_year(dates)
```

### Procurement methods used

```{code-cell}
%%sql
SELECT
    procurementmethod,
    count(DISTINCT ocid),
    round((count(*) * 100.0 / sum(count(*)) OVER ()), 1) AS proportion
FROM
    tender_summary
WHERE
    release_type = 'compiled_release'
GROUP BY
    procurementmethod
ORDER BY
    proportion DESC
```

```{code-cell}
%%sql
SELECT
    tender ->> 'procurementMethodDetails' AS method,
    count(DISTINCT ocid),
    round((count(*) * 100.0 / sum(count(*)) OVER ()), 1) AS proportion
FROM
    tender_summary
WHERE
    release_type = 'compiled_release'
GROUP BY
    method
ORDER BY
    proportion DESC
```

### Number of procedures by buyer

```{code-cell}
%%sql buyers <<
SELECT
    identifier AS party_id,
    party -> 'name' AS name,
    count(DISTINCT ocid) AS total_tenders
FROM
    parties_summary
WHERE
    roles::text ILIKE '%%buyer%%'
    AND release_type = 'compiled_release'
GROUP BY
    identifier,
    party -> 'name'
ORDER BY
    total_tenders DESC
```

```{code-cell}
buyers.head(10)
```

```{code-cell}
plot_top_buyers(buyers.head(10))
```
