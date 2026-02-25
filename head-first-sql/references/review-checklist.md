# SQL Review Checklist

Use this checklist when reviewing SQL queries or schemas.

## Correctness

- [ ] Are JOIN conditions complete and correct? (No missing ON clause → no Cartesian product)
- [ ] Is `IS NULL` / `IS NOT NULL` used instead of `= NULL` / `!= NULL`?
- [ ] Is WHERE used for row-level filters and HAVING for aggregate filters?
- [ ] Does the query handle NULLs correctly in aggregate functions? (COUNT(*) vs COUNT(column))
- [ ] Are all columns in SELECT either in GROUP BY or inside an aggregate function?
- [ ] Does LEFT JOIN logic correctly identify unmatched rows (check for `IS NULL` on right table's key)?
- [ ] Are INNER JOIN vs LEFT JOIN vs RIGHT JOIN types correct for the intended result?
- [ ] Does the query return distinct rows when duplicates are expected to be eliminated?

## Readability

- [ ] Are explicit column names used instead of `SELECT *`?
- [ ] Are meaningful aliases given to tables (`c` for `customers`) and computed columns (`AS order_count`)?
- [ ] Is explicit JOIN syntax used instead of comma-separated tables in FROM?
- [ ] Is the query formatted consistently (indented, one clause per line)?
- [ ] Are complex conditions broken across multiple lines for readability?

## Performance

- [ ] Are there full-table scans on large tables that an index could eliminate?
- [ ] Are WHERE conditions on indexed columns written in a sargable form? (No function wrapping: use `WHERE created_at >= '2024-01-01'` not `WHERE YEAR(created_at) = 2024`)
- [ ] Is there a correlated subquery that runs once per row? (Rewrite with JOIN + GROUP BY)
- [ ] Is DISTINCT used as a band-aid for a bad JOIN? (Investigate the duplication source instead)
- [ ] Are indexes present on columns used in JOIN ON, WHERE, and ORDER BY?
- [ ] Is LIMIT used for result sets that don't need to return all rows?

## Safety

- [ ] Are multi-step writes (INSERT + UPDATE + DELETE sequences) wrapped in a transaction?
- [ ] Is ROLLBACK logic present for error cases?
- [ ] Are queries built with parameterized placeholders, not string concatenation?
- [ ] Do DELETE / UPDATE statements have a WHERE clause? (Bare DELETE FROM table deletes all rows)

## Schema Design

- [ ] Is there a primary key on every table?
- [ ] Are foreign key constraints defined to enforce referential integrity?
- [ ] Is data normalized — no repeating groups, no comma-separated IDs in a single column?
- [ ] Are column names clear and consistent (snake_case, singular nouns for entity columns)?
- [ ] Are NOT NULL constraints used on columns that should never be empty?
- [ ] Is COALESCE used to provide defaults for nullable columns in SELECT?
