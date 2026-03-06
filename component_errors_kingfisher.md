## Check for data collection and processing errors

Kingfisher Collect and Kingfisher Process log messages that might indicate OCDS implementation errors or API stability issues.

Confirm any errors or warnings by manually checking the OCDS publication.

### Kingfisher Collect

See [how to review the Kingfisher Collect crawl's log file](https://kingfisher-collect.readthedocs.io/en/latest/logs.html).

**Note:** There is an open [pull request](https://github.com/open-contracting/notebooks-ocds/pull/44) to automate this. If interested, please comment on the pull request to prioritize it.

### Kingfisher Process

Users add a note when starting a crawl and when running the `load` command.

Kingfisher Process adds notes (the `note` column) at different levels (the `code` column):

- `INFO`
  - *load*: The Kingfisher Collect crawl's reason for closing and statistics (the `data` column).
- `WARNING`
  - *compile*: When a record has undated releases, linked releases or no releases, but a compiled release can be calculated (by merging remaining dated releases, using the `compiledRelease` field, or using an undated release with a 'compiled' tag).
- `ERROR`
  - *load*: When the input data is invalid JSON.
  - *compile*: When no compiled release can be calculated for a record.

📗 **You can check the full list of note types and what they mean in the Kingfisher Process's [documentation](https://kingfisher-process.readthedocs.io/en/latest/database.html#collection-note-table)**📗

List the notes for each of your collections:

```sql
SELECT
    collection_id,
    code,
    note,
    data
FROM
    collection_note
WHERE
    collection_id IN :collection_ids
```
