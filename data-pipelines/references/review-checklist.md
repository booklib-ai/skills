# Data Pipelines Pocket Reference — Pipeline Review Checklist

Systematic checklist for reviewing data pipelines against the 13 chapters
from *Data Pipelines Pocket Reference* by James Densmore.

---

## 1. Architecture & Patterns (Chapters 1–3)

### Infrastructure
- [ ] **Ch 1-2 — Appropriate infrastructure** — Is the right storage chosen for the use case (warehouse for analytics, lake for raw/unstructured)?
- [ ] **Ch 2 — Cloud-native services** — Are managed services used where appropriate to reduce operational burden?
- [ ] **Ch 2 — Separation of storage and compute** — Is compute scaled independently from storage?

### Pipeline Patterns
- [ ] **Ch 3 — ETL vs ELT** — Is the right pattern chosen? Is ELT used for analytics workloads with modern warehouses?
- [ ] **Ch 3 — Full vs incremental** — Is incremental extraction used for growing datasets? Is full extraction justified for small tables?
- [ ] **Ch 3 — CDC where appropriate** — Is CDC used for real-time sync needs instead of polling?
- [ ] **Ch 3 — Loading strategy** — Is the right load pattern used (append for events, upsert for dimensions, full refresh for small lookups)?

---

## 2. Data Ingestion (Chapters 4–7)

### Database Ingestion (Ch 4)
- [ ] **Ch 4 — Read replica usage** — Are extractions running against read replicas, not production databases?
- [ ] **Ch 4 — Incremental column** — Is there a reliable timestamp or ID column for incremental extraction?
- [ ] **Ch 4 — Connection management** — Are connections pooled and properly closed? Are timeouts configured?
- [ ] **Ch 4 — Query efficiency** — Are only needed columns selected? Are WHERE clauses using indexed columns?
- [ ] **Ch 4 — Large table handling** — Are large extractions chunked or using streaming cursors?

### File Ingestion (Ch 5)
- [ ] **Ch 5 — Schema validation** — Are file schemas validated before processing? Are malformed rows handled?
- [ ] **Ch 5 — Encoding handling** — Is character encoding handled consistently (UTF-8)?
- [ ] **Ch 5 — Cloud storage patterns** — Are files organized with partitioned prefixes? Are processed files archived?
- [ ] **Ch 5 — File tracking** — Is there a mechanism to track which files have been processed to avoid reprocessing?
- [ ] **Ch 5 — Compression** — Are files compressed for storage and transfer efficiency?

### API Ingestion (Ch 6)
- [ ] **Ch 6 — Pagination** — Is pagination implemented correctly? Are all pages fetched? Is cursor-based preferred?
- [ ] **Ch 6 — Rate limiting** — Are rate limit headers respected? Is backoff implemented for 429 responses?
- [ ] **Ch 6 — Retry logic** — Are transient errors (5xx, timeouts) retried with exponential backoff? Are 4xx errors not retried?
- [ ] **Ch 6 — Authentication** — Are credentials stored securely? Are token refreshes handled?
- [ ] **Ch 6 — Incremental fetching** — Are date/cursor parameters used to fetch only new data?

### Streaming Ingestion (Ch 7)
- [ ] **Ch 7 — Consumer group design** — Are consumer groups configured for parallel processing? Are rebalances handled?
- [ ] **Ch 7 — Offset management** — Are offsets committed after successful processing, not before?
- [ ] **Ch 7 — Serialization** — Are events serialized with a schema (Avro, Protobuf) for evolution support?
- [ ] **Ch 7 — Dead letter queue** — Are failed events routed to a DLQ for inspection and reprocessing?
- [ ] **Ch 7 — Exactly-once semantics** — Is deduplication implemented downstream or are idempotent producers used?
- [ ] **Ch 7 — Backpressure** — Is backpressure handled when consumer can't keep up with producer?

---

## 3. Data Storage & Loading (Chapter 8)

### Loading Patterns
- [ ] **Ch 8 — Bulk loading** — Are bulk load commands used (COPY, load jobs) instead of row-by-row INSERT?
- [ ] **Ch 8 — Staging tables** — Is data loaded to staging first, validated, then merged to production?
- [ ] **Ch 8 — Atomic operations** — Are loads atomic? Is the destination never left in a partial state?
- [ ] **Ch 8 — Data type mapping** — Are source types mapped correctly to destination types? No implicit conversions?

### Table Design
- [ ] **Ch 8 — Partitioning** — Are large tables partitioned by date or key? Are queries leveraging partition pruning?
- [ ] **Ch 8 — Clustering** — Are frequently filtered columns used as cluster keys within partitions?
- [ ] **Ch 8 — Sort/distribution keys** — For Redshift: are SORTKEY and DISTKEY chosen based on query patterns?

### Warehouse-Specific
- [ ] **Ch 8 — Redshift COPY** — Is S3-based COPY used instead of INSERT for bulk loads?
- [ ] **Ch 8 — BigQuery load jobs** — Are load jobs preferred over streaming inserts for batch pipelines?
- [ ] **Ch 8 — Snowflake stages** — Are stages used for file-based loading? Is SNOWPIPE configured for continuous loads?

---

## 4. Transformations (Chapter 9)

### SQL Transforms
- [ ] **Ch 9 — CTEs for readability** — Are Common Table Expressions used instead of deeply nested subqueries?
- [ ] **Ch 9 — Window functions** — Are window functions used for ranking, running totals instead of self-joins?
- [ ] **Ch 9 — Grain awareness** — Do joins maintain the correct grain? No accidental fan-out producing duplicate rows?
- [ ] **Ch 9 — Deterministic logic** — Are transforms deterministic (same input → same output)? No reliance on row ordering?

### dbt Patterns
- [ ] **Ch 9 — Layer structure** — Are models organized into staging → intermediate → mart layers?
- [ ] **Ch 9 — Staging models** — Are staging models 1:1 with sources? Do they rename, cast, and filter only?
- [ ] **Ch 9 — Incremental models** — Are large models configured as incremental with proper `unique_key` and merge strategy?
- [ ] **Ch 9 — Source definitions** — Are sources defined in YAML with `source()` macro? Are freshness checks configured?
- [ ] **Ch 9 — Model materialization** — Are materializations appropriate (view for light transforms, table for heavy, incremental for large)?

### Python Transforms
- [ ] **Ch 9 — Appropriate tool** — Is Python used only when SQL is insufficient (ML, complex parsing, API calls)?
- [ ] **Ch 9 — Vectorized operations** — Are pandas/numpy vectorized operations used instead of row-by-row iteration?
- [ ] **Ch 9 — Memory management** — Are large datasets processed in chunks or with distributed frameworks (PySpark)?
- [ ] **Ch 9 — Pure functions** — Are transformation functions pure (no side effects) and independently testable?

---

## 5. Data Validation & Testing (Chapter 10)

### Validation Coverage
- [ ] **Ch 10 — Schema validation** — Are column names, types, and count validated at ingestion?
- [ ] **Ch 10 — Row count reconciliation** — Are source and destination row counts compared? Is threshold alerting configured?
- [ ] **Ch 10 — Null checks** — Are NOT NULL constraints enforced on key columns? Are null percentages tracked?
- [ ] **Ch 10 — Uniqueness checks** — Is primary key uniqueness verified after loading?
- [ ] **Ch 10 — Referential integrity** — Are foreign key relationships validated between related tables?
- [ ] **Ch 10 — Range validation** — Are values checked against expected ranges (dates in past, amounts positive, percentages 0-100)?
- [ ] **Ch 10 — Freshness checks** — Is data freshness monitored? Are alerts configured for stale data?

### Testing
- [ ] **Ch 10 — Unit tests** — Are individual transformation functions tested with known inputs/outputs?
- [ ] **Ch 10 — Integration tests** — Is the end-to-end pipeline tested with sample data?
- [ ] **Ch 10 — dbt tests** — Are dbt schema tests (not_null, unique, relationships) defined? Are custom data tests used?
- [ ] **Ch 10 — Regression tests** — Are current results compared against known-good baselines for critical tables?

---

## 6. Orchestration (Chapter 11)

### DAG Design
- [ ] **Ch 11 — One pipeline per DAG** — Are DAGs focused on a single pipeline? No mega-DAGs?
- [ ] **Ch 11 — Task granularity** — Are tasks atomic and independently retryable? Not too fine or too coarse?
- [ ] **Ch 11 — Shallow and wide** — Are DAGs shallow (few sequential steps) and wide (parallel where possible)?
- [ ] **Ch 11 — No hardcoded dates** — Are dates parameterized using execution_date or equivalent? No hardcoded date strings?

### Airflow Specifics
- [ ] **Ch 11 — Idempotent tasks** — Can every task be safely re-run without data duplication or side effects?
- [ ] **Ch 11 — Appropriate operators** — Are provider operators used where available instead of generic PythonOperator?
- [ ] **Ch 11 — XCom usage** — Are XComs used only for small metadata (file paths, row counts), not large data?
- [ ] **Ch 11 — Sensor timeouts** — Do sensors have timeouts to avoid indefinite waiting?
- [ ] **Ch 11 — Error callbacks** — Are `on_failure_callback` configured for alerting on task failures?
- [ ] **Ch 11 — Retries** — Are retries configured with appropriate delay for transient failures?
- [ ] **Ch 11 — Pool limits** — Are pools used to limit concurrency for resource-constrained tasks?
- [ ] **Ch 11 — Catchup configuration** — Is `catchup` set appropriately (True for backfill-supporting DAGs, False otherwise)?

---

## 7. Monitoring & Operations (Chapters 12–13)

### Monitoring
- [ ] **Ch 12 — Duration tracking** — Is pipeline execution time tracked and alerted on anomalies?
- [ ] **Ch 12 — Row count monitoring** — Are rows processed per run tracked? Alerts on zero or unusual counts?
- [ ] **Ch 12 — Error rate tracking** — Are failed records, retries, and exceptions monitored?
- [ ] **Ch 12 — Data freshness SLA** — Are freshness SLAs defined and monitored? Alerts on breaches?
- [ ] **Ch 12 — Resource monitoring** — Are CPU, memory, disk, and network usage tracked for pipeline infrastructure?

### Alerting
- [ ] **Ch 12 — Actionable alerts** — Do alerts include context (error message, affected table, run ID, link to logs)?
- [ ] **Ch 12 — Severity levels** — Are alerts classified by severity with appropriate routing?
- [ ] **Ch 12 — Alert fatigue prevention** — Are thresholds tuned to avoid noisy alerts? Are alerts deduplicated?

### Operational Excellence
- [ ] **Ch 13 — Idempotency** — Are all pipelines idempotent? Can they be re-run without data corruption?
- [ ] **Ch 13 — Backfill support** — Are pipelines parameterized for date-range backfilling?
- [ ] **Ch 13 — Error handling** — Are transient errors retried? Are permanent errors failed fast? Are bad records quarantined?
- [ ] **Ch 13 — Credential security** — Are credentials in secrets managers, not in code or config files?
- [ ] **Ch 13 — Data lineage** — Is source-to-destination mapping documented? Is transformation logic recorded?
- [ ] **Ch 13 — Documentation** — Is there a README, data dictionary, and runbook for each pipeline?
- [ ] **Ch 13 — Version control** — Is all pipeline code in git? Are changes reviewed via PR?

---

## Quick Review Workflow

1. **Architecture pass** — Verify ETL/ELT choice, incremental vs full, infrastructure fit
2. **Ingestion pass** — Check source-specific best practices, error handling, incremental logic
3. **Loading pass** — Verify bulk loading, staging tables, partitioning, atomic operations
4. **Transform pass** — Check SQL quality, dbt patterns, layer structure, determinism
5. **Validation pass** — Verify data quality checks at each boundary, test coverage
6. **Orchestration pass** — Check DAG design, idempotency, task granularity, error handling
7. **Operations pass** — Verify monitoring, alerting, backfill support, documentation
8. **Prioritize findings** — Rank by severity: data loss risk > data quality > performance > best practices > style

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Data loss, corruption, or security risk | Non-idempotent pipeline causing duplicates, hardcoded credentials, no staging tables with partial load risk, missing dead letter queue losing events |
| **High** | Data quality or reliability issues | Missing validation, no error handling, full extraction on large tables, no monitoring or alerting, blocking on rate limits |
| **Medium** | Performance, maintainability, or operational gaps | Missing partitioning, monolithic DAGs, no backfill support, missing documentation, no incremental models for large tables |
| **Low** | Best practice improvements, optimization opportunities | Missing compression, suboptimal clustering, verbose logging, minor naming inconsistencies |
