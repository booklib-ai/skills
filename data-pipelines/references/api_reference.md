# Data Pipelines Pocket Reference — Practices Catalog

Chapter-by-chapter catalog of practices from *Data Pipelines Pocket Reference*
by James Densmore for pipeline building.

---

## Chapter 1–2: Introduction & Modern Data Infrastructure

### Infrastructure Choices
- **Data warehouse** — Columnar storage optimized for analytics queries (Redshift, BigQuery, Snowflake); choose when analytics is primary use case
- **Data lake** — Object storage (S3, GCS, Azure Blob) for raw, unstructured, or semi-structured data; choose when data variety is high or schema is unknown
- **Hybrid** — Land raw data in lake, load structured subsets into warehouse; common modern pattern
- **Cloud-native** — Leverage managed services (serverless compute, auto-scaling storage); reduce operational burden

### Pipeline Types
- **Batch** — Process data in scheduled intervals (hourly, daily); suitable for most analytics use cases
- **Streaming** — Process data continuously as it arrives; required for real-time dashboards, alerts, event-driven systems
- **Micro-batch** — Small frequent batches (every few minutes); compromise between batch simplicity and near-real-time latency

---

## Chapter 3: Common Data Pipeline Patterns

### Extraction Patterns
- **Full extraction** — Extract entire dataset each run; simple but expensive for large tables; use for small reference tables or initial loads
- **Incremental extraction** — Extract only new/changed records using a high-water mark (timestamp, auto-increment ID, or sequence); preferred for growing datasets
- **Change data capture (CDC)** — Capture changes from database transaction logs (MySQL binlog, PostgreSQL WAL); lowest latency, captures deletes; use for real-time sync

### Loading Patterns
- **Full refresh (truncate + load)** — Replace entire destination table; simple, idempotent; use for small tables or when incremental is unreliable
- **Append** — Insert new records only; use for event/log data that is never updated
- **Upsert (MERGE)** — Insert new records, update existing ones based on a key; use for mutable dimension data
- **Delete + Insert by partition** — Delete partition, insert replacement; idempotent and efficient for date-partitioned fact tables

### ETL vs ELT
- **ETL** — Transform before loading; use when destination has limited compute or when data must be cleansed before storage
- **ELT** — Load raw data first, transform in destination; preferred for modern cloud warehouses with cheap compute; enables raw data preservation and flexible re-transformation

---

## Chapter 4: Database Ingestion

### MySQL Extraction
- Use `SELECT ... WHERE updated_at > :last_run` for incremental extraction
- For full extraction: `SELECT *` with optional `LIMIT/OFFSET` for large tables (prefer streaming cursors)
- Use read replicas to avoid impacting production database performance
- Handle MySQL timezone conversions (store/compare in UTC)
- Connection pooling for concurrent extraction from multiple tables

### PostgreSQL Extraction
- Similar incremental patterns using timestamp columns
- Use `COPY TO` for efficient bulk export to CSV/files
- Leverage PostgreSQL logical replication for CDC
- Handle PostgreSQL-specific types (arrays, JSON, custom types) during extraction

### MongoDB Extraction
- Use change streams for real-time CDC
- For incremental: query by `_id` (ObjectId contains timestamp) or custom timestamp field
- Handle nested documents: flatten or store as JSON in warehouse
- Use `mongodump` for full extraction of large collections

### General Database Practices
- **Connection management** — Use connection pools; close connections promptly; handle timeouts
- **Query optimization** — Add indexes on extraction columns; limit selected columns; use WHERE clauses
- **Binary data** — Skip or store references to BLOBs; don't load binary into analytics warehouse
- **Character encoding** — Ensure UTF-8 throughout the pipeline; handle encoding mismatches at extraction

---

## Chapter 5: File Ingestion

### CSV Files
- Handle header rows, quoting, escaping, delimiters (not always comma)
- Detect and handle encoding (UTF-8, Latin-1, Windows-1252)
- Validate column count per row; log and quarantine malformed rows
- Use streaming parsers for large files; avoid loading entire file into memory

### JSON Files
- Handle nested structures: flatten for warehouse loading or store as JSON column
- Use JSON Lines (newline-delimited JSON) for large datasets
- Validate against expected schema; handle missing and extra fields
- Parse dates and timestamps consistently

### Cloud Storage Integration
- **S3** — Use `aws s3 cp/sync` or boto3; leverage S3 event notifications for trigger-based ingestion
- **GCS** — Use `gsutil` or google-cloud-storage library; use Pub/Sub for event notifications
- **Azure Blob** — Use Azure SDK; leverage Event Grid for notifications
- Use prefix/partition naming: `s3://bucket/table/year=2024/month=01/day=15/`
- Implement file manifests to track which files have been processed

### File Best Practices
- **Naming conventions** — Include date, source, and sequence in filenames: `orders_2024-01-15_001.csv`
- **Compression** — Use gzip or snappy for storage efficiency; most tools handle compressed files natively
- **Archiving** — Move processed files to archive prefix/bucket; retain for reprocessing capability
- **Schema detection** — Infer schema from first N rows; validate against expected schema; alert on changes

---

## Chapter 6: API Ingestion

### REST API Patterns
- **Authentication** — Handle API keys, OAuth tokens, token refresh; store credentials securely
- **Pagination** — Implement cursor-based, offset-based, or link-header pagination; prefer cursor-based for consistency
- **Rate limiting** — Respect rate limit headers (X-RateLimit-Remaining, Retry-After); implement backoff
- **Retry logic** — Retry on 429 (rate limit) and 5xx (server error) with exponential backoff; don't retry on 4xx (client error)

### API Data Handling
- **JSON response parsing** — Extract relevant fields; handle nested objects and arrays
- **Incremental fetching** — Use modified_since parameters, cursor tokens, or date range filters
- **Schema changes** — Handle new fields gracefully; log and alert on missing expected fields
- **Large responses** — Stream responses for large payloads; paginate aggressively

### Webhook Ingestion
- Set up HTTP endpoints to receive push notifications
- Validate webhook signatures for security
- Acknowledge receipt quickly (200 OK); process asynchronously
- Implement idempotency using event IDs to handle duplicate deliveries

---

## Chapter 7: Streaming Data

### Apache Kafka
- **Producers** — Serialize events (Avro, JSON, Protobuf); use keys for partition ordering; configure acknowledgments
- **Consumers** — Use consumer groups for parallel processing; commit offsets after successful processing; handle rebalances
- **Topics** — Design topic schemas; set retention policies; partition for throughput and ordering requirements
- **Exactly-once** — Use idempotent producers + transactional consumers; or implement deduplication downstream

### Amazon Kinesis
- **Streams** — Configure shard count for throughput; use enhanced fan-out for multiple consumers
- **Firehose** — Direct-to-S3/Redshift delivery; configure buffering interval and size; transform with Lambda

### Stream Processing Patterns
- **Windowing** — Tumbling, sliding, session windows for aggregation over time
- **Watermarks** — Handle late-arriving events; define allowed lateness
- **State management** — Use state stores for aggregations; handle checkpointing and recovery
- **Dead letter queues** — Route failed events for inspection and reprocessing; don't lose data silently

---

## Chapter 8: Data Storage and Loading

### Amazon Redshift
- Use `COPY` command for bulk loading from S3; much faster than INSERT
- Define `SORTKEY` for frequently filtered columns; `DISTKEY` for join columns
- Use `UNLOAD` for efficient export back to S3
- Vacuum and analyze tables after large loads

### Google BigQuery
- Use load jobs for bulk data; streaming inserts for real-time (more expensive)
- Partition tables by date (ingestion time or column-based) for cost and performance
- Cluster tables on frequently filtered columns
- Use external tables for querying data in GCS without loading

### Snowflake
- Use stages (internal or external) for file-based loading
- `COPY INTO` for bulk loads from stages; `SNOWPIPE` for continuous loading
- Use virtual warehouses sized appropriately for load workloads
- Leverage Time Travel for data recovery and auditing

### General Loading Practices
- **Staging tables** — Always load to staging first; validate before merging to production
- **Atomic swaps** — Use table rename or partition swap for atomic updates
- **Data types** — Map source types carefully; avoid implicit conversions; use appropriate precision
- **Compression** — Let warehouse handle compression; load compressed files when supported
- **Partitioning** — Partition by date for time-series data; by key for lookup tables
- **Clustering** — Cluster on frequently filtered columns within partitions

---

## Chapter 9: Data Transformations

### SQL-Based Transforms
- Use CTEs (Common Table Expressions) for readability
- Prefer window functions over self-joins for ranking, running totals
- Use CASE expressions for conditional logic
- Aggregate at the right grain; avoid fan-out joins that multiply rows

### dbt (Data Build Tool)
- **Staging models** — 1:1 with source tables; rename columns, cast types, filter deleted records
- **Intermediate models** — Business logic joins, complex calculations, deduplication
- **Mart models** — Final analytics-ready tables; optimized for dashboard queries
- **Incremental models** — Process only new/changed data; use `unique_key` for merge strategy
- **Tests** — `not_null`, `unique`, `accepted_values`, `relationships` on key columns; custom data tests
- **Sources** — Define sources in YAML; use `source()` macro for lineage tracking; freshness checks

### Python-Based Transforms
- Use pandas for small-medium datasets; PySpark or Dask for large-scale processing
- Write pure functions for transformations; make them testable
- Handle data types explicitly; don't rely on inference for production pipelines
- Use vectorized operations; avoid row-by-row iteration

### Transform Best Practices
- **Layered architecture** — Raw → Staging → Intermediate → Mart; each layer has clear purpose
- **Single responsibility** — Each model/transform does one thing well
- **Documented logic** — Comment complex business rules; maintain a data dictionary
- **Version controlled** — All transformation code in git; review changes via PR

---

## Chapter 10: Data Validation and Testing

### Validation Types
- **Schema validation** — Verify column names, types, and count match expectations
- **Row count checks** — Compare source and destination row counts; alert on significant discrepancies
- **Null checks** — Assert key columns are not null; track null percentages for optional columns
- **Uniqueness checks** — Verify primary key uniqueness in destination tables
- **Referential integrity** — Check foreign key relationships between tables
- **Range checks** — Validate values fall within expected ranges (dates, amounts, percentages)
- **Freshness checks** — Verify data is not stale; alert when max timestamp is older than threshold

### Great Expectations
- Define expectations as code; version control them
- Run validations as pipeline steps; fail pipeline on critical expectation failures
- Generate data documentation from expectations
- Use checkpoints for scheduled validation runs

### Testing Practices
- **Unit tests** — Test individual transformation functions with known inputs/outputs
- **Integration tests** — Test end-to-end pipeline with sample data
- **Regression tests** — Compare current results against known-good baselines
- **Data contracts** — Define and enforce schemas between producer and consumer teams

---

## Chapter 11: Orchestration

### Apache Airflow
- **DAGs** — Define pipelines as Directed Acyclic Graphs; each node is a task
- **Operators** — Use appropriate operators: PythonOperator, BashOperator, provider operators (BigQueryOperator, S3ToRedshiftOperator)
- **Scheduling** — Use cron expressions or timedelta; set `start_date` and `catchup` appropriately
- **Dependencies** — Use `>>` operator or `set_upstream/downstream`; keep DAGs shallow and wide
- **XComs** — Pass small metadata between tasks (row counts, file paths); NOT large datasets
- **Sensors** — Wait for external conditions (file arrival, partition availability); use with timeout
- **Variables and Connections** — Store config in Airflow Variables; credentials in Connections
- **Pools** — Limit concurrency for resource-constrained tasks (database connections, API rate limits)

### DAG Design Patterns
- **One pipeline per DAG** — Keep DAGs focused; avoid mega-DAGs that do everything
- **Idempotent tasks** — Every task can be re-run safely; use `execution_date` for parameterization
- **Task granularity** — Tasks should be atomic and independently retryable; not too fine (overhead) or coarse (blast radius)
- **Error handling** — Use `on_failure_callback` for alerting; `retries` and `retry_delay` for transient failures
- **Backfilling** — Use `airflow backfill` for historical reprocessing; ensure tasks support date parameterization

---

## Chapter 12: Monitoring and Alerting

### Pipeline Health Metrics
- **Duration** — Track execution time; alert on runs significantly longer than historical average
- **Row counts** — Track records processed per run; alert on zero rows or dramatic changes
- **Error rates** — Track failed records, retries, exceptions; alert on elevated error rates
- **Data freshness** — Track max timestamp in destination; alert when data is staler than SLA
- **Resource usage** — Track CPU, memory, disk, network; alert on resource exhaustion

### Alerting Strategies
- **SLA-based** — Define delivery SLAs; alert when pipelines miss their windows
- **Anomaly-based** — Detect deviations from historical patterns (row counts, durations, values)
- **Threshold-based** — Alert on fixed thresholds (error rate > 5%, null rate > 10%)
- **Escalation** — Define severity levels; route alerts appropriately (Slack, PagerDuty, email)

### Logging
- Log at each pipeline stage: extraction start/end, row counts, load confirmation
- Include correlation IDs to trace records through the pipeline
- Store logs centrally for searchability (ELK, CloudWatch, Stackdriver)
- Retain logs for debugging and audit compliance

---

## Chapter 13: Best Practices

### Idempotency
- Use DELETE+INSERT by date partition for fact tables
- Use MERGE/upsert with natural keys for dimension tables
- Use staging tables as intermediary; clean up on both success and failure
- Test by running pipeline twice; verify no data duplication

### Backfilling
- Parameterize all pipelines by date range (start_date, end_date)
- Use Airflow `execution_date` or equivalent for date-aware runs
- Test backfill on a small date range before running full historical reprocess
- Monitor resource usage during backfill; may need to throttle parallelism

### Error Handling
- Retry transient failures (network timeouts, rate limits) with exponential backoff
- Fail fast on permanent errors (authentication failure, missing source table)
- Quarantine bad records; don't let one bad row fail the entire pipeline
- Send alerts with actionable context (error message, affected table, run ID)

### Data Lineage and Documentation
- Track source-to-destination mappings for every table
- Document transformation logic, especially business rules
- Maintain a data dictionary with column descriptions and types
- Use tools like dbt docs, DataHub, or Amundsen for automated lineage

### Security
- Never hardcode credentials; use secrets managers (AWS Secrets Manager, HashiCorp Vault)
- Encrypt data in transit (TLS) and at rest (warehouse encryption)
- Use least-privilege IAM roles for pipeline service accounts
- Audit access to sensitive data; mask PII in non-production environments
