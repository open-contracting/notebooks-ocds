## Perform manual data quality checks

[Pelican](https://ocdsdeploy.readthedocs.io/en/latest/use/pelican.html) performs dozens of data quality checks that can be exported to Google Docs. It performs checks on compiled releases, not on individual releases, records, or package metadata.

Use this section to perform quality checks that require manual review, including:

* Package metadata
* Release metadata
* Free-text language (*can be added to Pelican if needed*)
* Change history
* Overfill
* Placeholder values
* Ground truth
* Identifier scheme preference
* Segmented field coverage

+++

### Metadata

+++

#### Package metadata

OCDS data must be published within either a [release package](https://standard.open-contracting.org/latest/en/schema/reference/#package-metadata) or a [record package](https://standard.open-contracting.org/latest/en/schema/records_reference/#package-metadata).

Use this section to check the values in the package metadata.

Look out for the following issues and report them to the publisher:

* Placeholder values
* Empty strings and objects
* Discrepancies in the package metadata between different releases

+++

Display the package metadata for each collection:

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    package_data -> 'version' AS ocds_version,
    package_data -> 'publisher' -> 'name' AS publisher_name,
    package_data -> 'publisher' -> 'name' -> 'scheme' AS publisher_scheme,
    package_data -> 'publisher' -> 'name' -> 'uid' AS publisher_uid,
    package_data -> 'publisher' -> 'name' -> 'uri' AS publisher_uri,
    package_data -> 'license' AS license,
    package_data -> 'publicationPolicy' AS publicationpolicy,
    count(*)
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND release_type <> 'compiled_release'
GROUP BY
    collection_id,
    release_type,
    publisher_name,
    publisher_scheme,
    publisher_uid,
    publisher_uri,
    license,
    publicationpolicy,
    ocds_version;
```

#### Release tags

> A release must be tagged to indicate whether it is about a planning process or a contracting process and, if it is about the latter, to indicate the stage of the contracting process to which it relates. (OCDS 1.2)

Use this section to check that release tags reflect the data included in each release.

Read the descriptions in the [codelist](https://standard.open-contracting.org/latest/en/schema/codelists/#release-tagf) to understand which sections can be provided for each tag.

Remember that releases can repeat information from previous releases.

+++

Count the number of times a section is published, for each release tag.

Note that this check only counts whether the section exists, not whether it contains any fields or objects, so the results may include empty objects (e.g. `planning`) and arrays (e.g. `awards`).

```{code-cell}
%%sql release_tag_section_summary <<
WITH contract_implementation AS (
    SELECT
        cs.collection_id,
        cs.release_type,
        tag,
        count(contract -> 'implementation') AS contract_implementation
    FROM
        contracts_summary AS cs
    LEFT JOIN release_summary USING (id)
    GROUP BY
        cs.collection_id, cs.release_type, tag
),

sections AS (
    SELECT
        collection_id,
        release_type,
        tag,
        count(*) AS release_count,
        count(release -> 'planning') AS planning,
        count(release -> 'tender') AS tender,
        count(release -> 'awards') AS award,
        count(release -> 'contracts') AS contract
    FROM
        release_summary
    GROUP BY
        collection_id,
        release_type,
        tag
)

SELECT
    collection_id,
    release_type,
    sections.tag,
    release_count,
    planning,
    tender,
    award,
    contract,
    contract_implementation
FROM
    sections
LEFT JOIN contract_implementation USING (collection_id, release_type, tag);
```

```{code-cell}
release_tag_section_summary
```

#### Release date

+++

Use this section to check that all releases do not share the same date.

+++

For each collection and release type, generate a [frequency table](https://en.wikipedia.org/wiki/Frequency_distribution) for release dates and report the top 5 most frequent dates:

```{code-cell}
query = """
SELECT
    date,
    count(*) AS release_count
FROM
    release_summary
WHERE
    collection_id = :collection_id
GROUP BY
    date
ORDER BY
    release_count DESC
LIMIT 5
"""

for collection_id in collection_ids:
    print(f"collection_id {collection_id}:")
    display(get_ipython().run_line_magic("sql", query))
```

#### Language

+++

> The default language of the data, from the open language codelist. A BCP47 language tag is allowed, if there is a user need for the additional information.

Use this section to check that the code declared in `language` reflects the language used in free-text fields in the data.

+++

List the language codes used, with an example release for each language.

```{code-cell}
%%sql
SELECT DISTINCT ON (
    collection_id, release_type,
    language)
    collection_id,
    release_type,
    language,
    release AS example_release
FROM
    release_summary
ORDER BY
    collection_id,
    release_type,
    language;
```

### Change history

+++

OCDS supports the publication of a change history, using [releases and records](https://standard.open-contracting.org/latest/en/primer/releases_and_records/).

Fully implemented, releases and records can be used to publish the following for each contracting process:

* Multiple releases, one for each change or update to the contracting process
* A single record, containing:
  * `releases`: an index of releases for the contracting process
  * optionally, a `compiledRelease`: the latest version of the data about the contracting process
  * optionally, a `versionedRelease`: a change history for each field

However, many publishers use the ['easy releases'](https://standard.open-contracting.org/latest/en/guidance/build/easy_releases/) approach: publish a single release per contracting process with the latest version of the data about the contracting process.

Use this section to understand the approach used by the publisher.

+++

#### Multiple releases per contracting process

+++

Use this section to:

* check if there are multiple releases per contracting process
* check the distribution of releases per contracting process
* examine examples of contracting processes with multiple releases

+++

Calculate statistics on the minimum, maximum, average and standard deviation of releases per contracting process.

```{code-cell}
query = """
WITH release_counts AS (
    SELECT
        ocid,
        count(*) AS release_count
    FROM
        release_summary
    WHERE
        collection_id = :collection_id
    GROUP BY
        ocid
)

SELECT
    min(release_count) AS min_releases_per_ocid,
    max(release_count) AS max_releases_per_ocid,
    round(avg(release_count), 2) AS avg_releases_per_ocid,
    round(stddev(release_count), 2) AS sd_releases_per_ocid
FROM
    release_counts;
"""

for collection_id in collection_ids:
    print(f"collection_id {collection_id}:")
    display(get_ipython().run_line_magic("sql", query))
```

Count the number of contracting processes, for each observed number of releases:

```{code-cell}
%%sql release_count_summary <<
WITH release_counts AS (
    SELECT
        collection_id,
        release_type,
        ocid,
        count(*) AS release_count
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('release', 'embedded_release')
    GROUP BY
        collection_id,
        release_type,
        ocid
)

SELECT
    collection_id,
    release_type,
    release_count,
    count(*) AS contracting_processes
FROM
    release_counts
GROUP BY
    collection_id,
    release_type,
    release_count;
```

```{code-cell}
release_count_summary
```

Plot the distribution of releases per contracting process:

```{code-cell}
%%sql release_counts <<
WITH release_counts AS (
    SELECT
        collection_id,
        release_type,
        ocid,
        count(*) AS release_count
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('release', 'embedded_release')
    GROUP BY
        collection_id,
        release_type,
        ocid
)

SELECT
    collection_id,
    release_type,
    release_count,
    count(*) AS ocid_count
FROM
    release_counts
GROUP BY
    collection_id,
    release_type,
    release_count;
```

```{code-cell}
plot_release_count(release_counts)
```

Create a release package containing the top 5 contracting processes with the most releases.

Specific things to check include:

* Does the `date` field differ between releases?
* Does the `tag` field differ between releases?

Also check for differences in which fields are provided for each release and for differences in the values of fields.

```{code-cell}
%%sql multiple_release_examples <<
WITH ranked_ocids AS (
    SELECT
        collection_id,
        release_type,
        ocid,
        count(*),
        row_number() OVER (
            PARTITION BY
                collection_id,
                release_type
            ORDER BY count(*) DESC
        ) AS row_number
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('release', 'embedded_release')
    GROUP BY
        collection_id,
        release_type,
        ocid
)

SELECT jsonb_build_object('releases', jsonb_agg(release)) AS release_package
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND release_type IN ('release', 'embedded_release')
    AND ocid IN (
        SELECT ocid
        FROM
            ranked_ocids
        WHERE
            row_number <= 5
    );
```

```{code-cell}
render_json(multiple_release_examples["release_package"][0])
```

To ease review, uncomment the following cell to convert the release package to a Google Sheet:

```{code-cell}
# Replace 'SPREADSHEET_NAME', as appropriate.
# save_dataframe_to_spreadsheet(multiple_release_examples, 'SPREADSHEET_NAME_multiple_releases')
```

#### Static release ID

+++

The release identifier must be updated when the information about a contracting process changes.

A common error is to set the release ID to the same value as the `ocid`, to set it to a subset of the `ocid`, and to neglect to update it.

Use this section to check that the release ID differs from the `ocid`.

+++

List the releases where `id` and `ocid` have the same value:

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    ocid,
    release_id
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND (
        ocid = release_id
        OR ocid ILIKE '%%' || release_id || '%%'
    )
```

#### Duplicate release ID

```{code-cell}
%%sql
SELECT
    ocid,
    release_id,
    count(*) AS release_count
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
GROUP BY
    ocid,
    release_id
HAVING
    count(*) > 1
```

Export to Google Sheets the 5 release IDs with the most duplicates, and review them to determine whether the full release is duplicated or only the release ID.

```{code-cell}
%%sql duplicate_release_ids <<
WITH release_ids AS (
    SELECT
        collection_id,
        ocid,
        release_type,
        release_id,
        count(*) AS release_count,
        row_number() OVER (
            PARTITION BY
                collection_id,
                release_type
            ORDER BY count(*) DESC
        ) AS row_number
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
    GROUP BY
        collection_id,
        ocid,
        release_type,
        release_id
    HAVING
        count(*) > 1
)

SELECT jsonb_build_object('releases', jsonb_agg(release)) AS release_package
FROM
    release_summary
WHERE
    collection_id IN :collection_ids
    AND release_type IN ('release', 'embedded_release')
    AND ocid IN (
        SELECT ocid
        FROM
            release_ids
        WHERE
            row_number <= 5
    );
```

```{code-cell}
render_json(duplicate_release_ids["release_package"][0])
```

```{code-cell}
# Replace 'SPREADSHEET_NAME', as appropriate.
# save_dataframe_to_spreadsheet(duplicate_release_ids, 'SPREADSHEET_NAME_duplicate_release_ids')
```

### Overfill

In a whole dataset, we expect there to be some differences between the values, items and dates listed in the tender, award and contract sections of OCDS.

In an effort to publish as many field as possible, publishers sometimes ignore semantics and map one field from their data source to several fields in OCDS, known as overfill.

Use this section to identify instances of overfill.

+++

#### Awards and contracts

Use this section to check if there are any differences between the following fields in the award and contract sections:

* `awards/date` and `contracts/dateSigned`
* `awards/value` and `contracts/value`
* `awards/items` and `contracts/items`
* `awards/contractPeriod` and `contracts/period`
* `award/documents` and `contracts/documents`

```{code-cell}
%%sql
SELECT
    contracts_summary.collection_id,
    contracts_summary.release_type,
    coalesce(
        awards_summary.date = contracts_summary.datesigned,
        FALSE
    ) AS date_match,
    coalesce(
        (awards_summary.value_amount = contracts_summary.value_amount)
        AND (awards_summary.value_currency = contracts_summary.value_currency),
        FALSE
    ) AS value_match,
    coalesce((
        awards_summary.contractperiod_startdate
        = contracts_summary.period_startdate
    )
    AND (
        awards_summary.contractperiod_enddate
        = contracts_summary.period_startdate
    ), FALSE) AS period_match,
    coalesce(
        awards_summary.award ->> 'documents'
        = contracts_summary.contract ->> 'documents',
        FALSE
    ) AS documents_match,
    count(contracts_summary.id) AS contract_count
FROM
    contracts_summary
INNER JOIN awards_summary
    ON
        contracts_summary.id = awards_summary.id
        AND contracts_summary.awardid = awards_summary.award_id
WHERE
    contracts_summary.collection_id IN :collection_ids
    AND contracts_summary.release_type IN ('record', 'compiled_release')
GROUP BY
    contracts_summary.collection_id,
    contracts_summary.release_type,
    date_match,
    value_match,
    period_match,
    documents_match
ORDER BY
    contracts_summary.collection_id ASC,
    contracts_summary.release_type ASC,
    contract_count DESC
```

#### Items

Items are attached to the tender, award and contract sections of a release, so that users can see if there were any changes to the items being procured during the contracting process.

Use this section to check for differences between the items attached to the tender, award and contract sections.

```{code-cell}
%%sql
SELECT
    tender_summary.collection_id,
    tender_summary.release_type,
    coalesce(
        contracts_summary.contract -> 'items'
        = awards_summary.award -> 'items',
        FALSE
    ) AS award_contract_match,
    count(contracts_summary.id) AS contracts_count,
    coalesce(
        awards_summary.award -> 'items'
        = tender_summary.tender -> 'items',
        FALSE
    ) AS tender_award_match,
    count(awards_summary.id) AS awards_count
FROM
    tender_summary
INNER JOIN awards_summary USING (id)
LEFT JOIN contracts_summary
    ON
        awards_summary.id = contracts_summary.id
        AND awards_summary.award_id = contracts_summary.awardid
WHERE
    tender_summary.collection_id IN :collection_ids
    AND tender_summary.release_type IN ('record', 'compiled_release')
GROUP BY
    tender_summary.collection_id,
    tender_summary.release_type,
    award_contract_match,
    tender_award_match;
```

### Placeholder values

Use this section to check for placeholder values.

Manually review the example release to identify placeholder values, e.g. 'n/a', 'test', '1970-01-01T00:00:00Z' etc.

+++

Get an example release:

```{code-cell}
%%sql example_releases <<
WITH examples AS (
    SELECT DISTINCT ON (
        collection_id,
        release_type)
        collection_id,
        release_type,
        release
    FROM
        release_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('release', 'embedded_release')
    ORDER BY
        collection_id,
        release_type,
        random()
)

SELECT jsonb_build_object('releases', jsonb_agg(release)) AS release_package
FROM
    examples
```

```{code-cell}
render_json(example_releases["release_package"][0])
```

### Ground truth

+++

#### Organization identifiers

+++

Publishers should collect and publish [organization identifiers](https://standard.open-contracting.org/latest/en/schema/identifiers/#organization-ids).

Use this section to check for invalid or incorrect organization identifiers. (Pelican checks schemes, not identifiers.)

For each organization identifier:

1. Look up the `scheme` in [org-id.guide](http://org-id.guide/) and follow the guidance to look up the organization identifiers in the register.
1. Check that the identifier exists in the register.

+++

Select a random sample of 3 identifiers for each organization identifier scheme:

```{code-cell}
%%sql organization_identifiers <<
SELECT
    collection_id,
    release_type,
    party ->> 'name' AS name,
    party -> 'identifier' ->> 'legalName' AS legalname,
    roles,
    party -> 'identifier' ->> 'scheme' AS scheme,
    party -> 'identifier' ->> 'id' AS id,
    ocid
FROM
    parties_summary
WHERE
    collection_id IN :collection_ids;
```

```{code-cell}
organization_identifiers.groupby(["collection_id", "release_type", "scheme"]).sample(n=3)
```

### Item classifications

+++

Use this section to check whether the data includes item classifications.

```{code-cell}
%%sql
WITH items AS (
    SELECT
        collection_id,
        release_type,
        'tender' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        tender_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
    UNION ALL
    SELECT
        collection_id,
        release_type,
        'award' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        award_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
    UNION ALL
    SELECT
        collection_id,
        release_type,
        'contract' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        contract_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
)

SELECT
    collection_id,
    release_type,
    stage,
    count(*) AS item_count,
    scheme
FROM
    items
GROUP BY
    collection_id,
    release_type,
    scheme,
    stage
ORDER BY stage;
```

Select a random sample of 3 identifiers for each item identifier scheme:

```{code-cell}
%%sql item_identifiers <<
WITH items AS (
    SELECT
        collection_id,
        release_type,
        'tender' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        tender_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
    UNION ALL
    SELECT
        collection_id,
        release_type,
        'award' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        award_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
    UNION ALL
    SELECT
        collection_id,
        release_type,
        'contract' AS stage,
        item -> 'classification' ->> 'id' AS id,
        item -> 'classification' ->> 'scheme' AS scheme
    FROM
        contract_items_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type = 'compiled_release'
)

SELECT *
FROM
    items
WHERE id IS NOT NULL;
```

```{code-cell}
item_identifiers.groupby(["collection_id", "release_type", "stage", "scheme"]).sample(n=3)
```

#### Document metadata

+++

Use this section to check that document metadata is accurate.

Retrieve the document from the `url` and check that each metadata field accurate reflects the actual document.




+++

Get a random document:

```{code-cell}
%%sql
WITH documents AS (
    SELECT
        collection_id,
        release_type,
        'planning' AS section,
        ocid,
        document
    FROM
        planning_documents_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
    UNION
    SELECT
        collection_id,
        release_type,
        'tender' AS section,
        ocid,
        document
    FROM
        tender_documents_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
    UNION
    SELECT
        collection_id,
        release_type,
        'awards' AS section,
        ocid,
        document
    FROM
        award_documents_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
    UNION
    SELECT
        collection_id,
        release_type,
        'contracts' AS section,
        ocid,
        document
    FROM
        contract_documents_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
    UNION
    SELECT
        collection_id,
        release_type,
        ocid,
        'implementation' AS section,
        document
    FROM
        contract_implementation_documents_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
)

SELECT DISTINCT ON (collection_id, release_type)
    collection_id,
    release_type,
    section,
    document ->> 'id' AS id,
    document ->> 'documentType' AS documenttype,
    document ->> 'title' AS title,
    document ->> 'description' AS description,
    document ->> 'url' AS url,
    document ->> 'datePublished' AS datepublished,
    document ->> 'dateModified' AS datemodified,
    document ->> 'format' AS format,
    document ->> 'language'
        AS
        language
FROM
    documents
ORDER BY
    collection_id,
    release_type;
```

### Identifier scheme preference

Publishers sometimes use a domestic register as the `.scheme` for foreign-registered companies. It is preferred to use an international register.

Use this section to check whether an international organization identifier scheme is provided for foreign-registered companies.

Set the `country` variable to the name of the country for the publisher before running the query.

For each organization identifier:

1. Look up the `scheme` in [org-id.guide](http://org-id.guide/) and follow the guidance to look up the organization identifiers in the register.
1. Check that the identifier exists in the register.

```{code-cell}
country = "Paraguay"
```

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    name,
    scheme,
    id,
    legalname,
    country,
    roles
FROM (
    SELECT DISTINCT
        collection_id,
        release_type,
        party ->> 'name' AS name,
        party -> 'identifier' ->> 'scheme' AS scheme,
        party -> 'identifier' ->> 'id' AS id,
        party -> 'identifier' ->> 'legalName' AS legalname,
        party -> 'address' ->> 'country' AS country,
        roles,
        rank()
            OVER (
                PARTITION BY
                    collection_id,
                    release_id,
                    party -> 'identifier' ->> 'scheme'
                ORDER BY random()
            )
    FROM parties_summary
    WHERE
        collection_id IN :collection_ids
        AND release_type IN ('record', 'compiled_release')
        AND party -> 'address' ->> 'country' NOT ILIKE :country
) AS identifiers
WHERE
    rank <= 3
ORDER BY
    scheme;
```

### Consistent party name-ID pairs across contracting processes

**Note**: This check will be [included in Pelican](https://github.com/open-contracting/pelican-backend/issues/28) and should be removed from here when implemented.

This section evaluates whether the parties section incorporates organizations with the same name but different identifiers, and whether there are organizations with the same ID but different names.

+++

#### Same ID with different names

Use this section to check that the party name remains consistent with its id across contracting processes.

Check the number of unique `parties/name` per `parties/identifier` (`parties/identifier/scheme` and `parties/identifier/id` pair) and `parties/role`.

```{code-cell}
%%sql
WITH id_per_name AS (
    SELECT
        identifier,
        roles,
        count(DISTINCT name) AS different_names
    FROM parties_summary
    WHERE
        release_type = 'release'
        AND
        identifier IS NOT NULL AND name IS NOT NULL
    GROUP BY identifier, roles
)

SELECT
    roles,
    count(*) AS total_names,
    count(*) FILTER (WHERE different_names > 1) AS ids_with_multiple_names
FROM id_per_name
GROUP BY roles
ORDER BY ids_with_multiple_names DESC;
```

Full list of parties with the same `parties/identifier` but different `parties/name`

```{code-cell}
%%sql
SELECT
    identifier,
    string_agg(DISTINCT name, '; ') AS names,
    count(DISTINCT name) AS total_names,
    roles
FROM parties_summary
WHERE
    release_type = 'release'
    AND identifier IS NOT NULL AND name IS NOT NULL
GROUP BY identifier, roles
HAVING count(DISTINCT name) > 1
ORDER BY total_names DESC;
```

#### Same name with different IDs

Use this section to check that the party id remains consistent with its name across contracting processes.

Check the number of unique `parties/identifer` (`parties/identifier/scheme` and `parties/identifier/id` pair) per `parties/name` and `parties/role`.

```{code-cell}
%%sql
WITH id_per_name AS (
    SELECT
        name,
        roles,
        count(DISTINCT identifier) AS different_ids
    FROM parties_summary
    WHERE
        release_type = 'release'
        AND
        identifier IS NOT NULL
    GROUP BY name, roles
)

SELECT
    roles,
    count(*) AS total_names,
    count(*) FILTER (WHERE different_ids > 1) AS names_with_multiple_ids
FROM id_per_name
GROUP BY roles
ORDER BY names_with_multiple_ids DESC;
```


Full list of parties with the same `parties/name` but different `parties/identifier`

```{code-cell}
%%sql
SELECT
    name,
    string_agg(DISTINCT identifier, ', ') AS identifiers,
    count(DISTINCT identifier) AS total_identifiers,
    roles
FROM parties_summary
WHERE
    release_type = 'release'
    AND identifier IS NOT NULL
GROUP BY name, roles
HAVING count(DISTINCT identifier) > 1;
```

### Coverage

Coverage is covered by Pelican. This section segments field coverage for priority fields (Pelican does not segment by, e.g., party role).

+++

Use this section to check whether the data includes key fields.

+++

#### Organization identifiers

+++

Use this section to check whether the data includes organization identifiers for buyers, procuring entities, suppliers and tenderers.

+++

Calculate the coverage of `parties/identifier/id` and `parties/identifier/scheme`, grouped by `parties/role`:

```{code-cell}
%%sql
SELECT
    collection_id,
    release_type,
    CASE
        WHEN roles @> '["buyer"]'::jsonb
            THEN
                'buyer'
        WHEN roles @> '["procuringEntity"]'::jsonb
            THEN
                'procuringEntity'
        WHEN roles @> '["supplier"]'::jsonb
            THEN
                'supplier'
        WHEN roles @> '["tenderer"]'::jsonb
            THEN
                'tenderer'
        ELSE
            'other'
    END AS role,
    count(*) AS party_count,
    round(sum(
        CASE
            WHEN party -> 'identifier' ->> 'id' IS NOT NULL
                THEN
                    1
            ELSE
                0
        END
    )::numeric / count(*), 2) AS id_coverage,
    round(sum(
        CASE
            WHEN party -> 'identifier' ->> 'scheme' IS NOT NULL
                THEN
                    1
            ELSE
                0
        END
    )::numeric / count(*), 2) AS scheme_coverage
FROM
    parties_summary
WHERE
    collection_id IN :collection_ids
    AND release_type = 'compiled_release'
GROUP BY
    collection_id,
    release_type,
    role;
```

### OCID modeling

+++

Use this section to check if the OCID is being modeled as expected

+++

#### Number of tenders per ocid

+++

Use this section to check there is always only one tender per ocid.

If the data contains planning data and multiple tenders per ocid, it might indicate that the ocid is being assigned in the planning stage, and the planning can have more than one tender, for example, due to unsuccessful tenders.

```{code-cell}
%%sql
SELECT
    ocid,
    count(DISTINCT data -> 'tender' ->> 'id') AS cnt
FROM data
INNER JOIN release ON data.id = data_id
WHERE collection_id IN :collection_ids
GROUP BY ocid
ORDER BY cnt DESC;
```
