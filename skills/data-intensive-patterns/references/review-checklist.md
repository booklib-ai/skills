# Data-Intensive Applications Code Review Checklist

Use this checklist when reviewing data-intensive application code. Work through each section
and flag any violations. Not every section applies to every review — skip sections
that aren't relevant to the code under review.

---

## 1. Data Modeling

- [ ] Data model fits the application's access patterns (relational, document, graph, event log)
- [ ] Relationships are modeled appropriately (joins vs. embedding vs. references)
- [ ] Schema is explicit or schema-on-read strategy is intentional and documented
- [ ] No impedance mismatch — application objects map cleanly to storage model
- [ ] Normalization level is appropriate (not over-normalized for a document store, not under-normalized for relational)

**Red flags**: Forcing graph-like traversals through a relational model with recursive joins.
Storing deeply nested JSON in a relational column then parsing it in application code.
Document model with many-to-many relationships handled by manual application-side joins.

---

## 2. Storage Engine and Indexing

- [ ] Storage engine matches workload characteristics (write-heavy → LSM; read-heavy → B-tree)
- [ ] Indexes exist for common query patterns
- [ ] No unnecessary indexes (each index slows down writes)
- [ ] Column-oriented storage used for analytical/OLAP workloads
- [ ] Materialized views or data cubes used where pre-aggregation helps
- [ ] Compaction strategy is configured appropriately for LSM-based stores

**Red flags**: Full table scans on large tables due to missing indexes. Using a row-oriented
store for analytical queries scanning millions of rows. Write-heavy workload on a database
optimized for reads without considering LSM alternatives.

---

## 3. Encoding and Schema Evolution

- [ ] Serialization format supports forward and backward compatibility
- [ ] Schema registry is in place for Avro/Protobuf-encoded messages
- [ ] Field tags (Protobuf) or schema resolution (Avro) used for evolution
- [ ] Old and new code can run simultaneously during rolling deployments
- [ ] No required fields added in a non-backward-compatible way
- [ ] Deleted field tags/names are never reused

**Red flags**: Using plain JSON for inter-service communication without versioning.
Adding required fields to Protobuf definitions in production. Encoding changes that break
consumers during rolling deployments. No schema registry for Kafka topics.

---

## 4. Replication

- [ ] Replication topology matches consistency and availability requirements
- [ ] Failover procedure is tested and documented
- [ ] Replication lag is monitored and handled in application code
- [ ] Read-after-write consistency is provided where needed (e.g., read from leader after write)
- [ ] Split-brain protection exists (fencing tokens, epoch numbers)
- [ ] For multi-leader: conflict resolution strategy is defined and tested
- [ ] For leaderless: quorum parameters (w, r, n) are tuned for the workload

**Red flags**: Async replication with no monitoring of replication lag. No split-brain protection
during leader failover. Using LWW for conflict resolution in multi-leader setup where data loss
is unacceptable. Quorum reads not configured (r + w ≤ n) giving inconsistent reads.

---

## 5. Partitioning

- [ ] Partition key distributes load evenly (no hot partitions)
- [ ] Partition strategy matches access patterns (key-range for scans, hash for uniform)
- [ ] Cross-partition queries are minimized or explicitly handled
- [ ] Secondary index strategy is chosen (local vs global) with trade-offs understood
- [ ] Rebalancing approach is defined (fixed partitions, dynamic split, proportional to nodes)
- [ ] Request routing is in place (client-side, routing tier, or coordinator)

**Red flags**: Monotonically increasing keys (timestamps, auto-increment) used as hash partition
key — all writes go to one partition. Range queries across hash-partitioned data. No plan
for rebalancing when adding nodes. Scatter-gather queries hitting all partitions for every read.

---

## 6. Transactions and Concurrency

- [ ] Isolation level is appropriate for the consistency requirements
- [ ] Write skew scenarios are identified and mitigated
- [ ] Phantom reads are prevented where needed (predicate/index-range locks or SSI)
- [ ] Long-running transactions are avoided (hold locks briefly)
- [ ] Deadlock detection or timeout is configured
- [ ] Optimistic concurrency (CAS, version numbers) used where appropriate

**Red flags**: Using READ COMMITTED where transactions read-then-write based on stale data
(write skew). SERIALIZABLE isolation everywhere regardless of need (performance waste).
Missing `SELECT ... FOR UPDATE` where concurrent updates can violate business rules.
No retry logic for serialization failures under SSI.

---

## 7. Distributed Systems Resilience

- [ ] All remote calls have timeouts configured
- [ ] Retries use exponential backoff with jitter
- [ ] Retry operations are idempotent (idempotency keys present)
- [ ] Circuit breakers protect against cascading failures
- [ ] Fencing tokens used for distributed locks/leases
- [ ] No reliance on wall-clock timestamps for ordering across nodes
- [ ] Network partitions are handled gracefully (not ignored)
- [ ] Process pauses (GC, etc.) are accounted for in lease/lock design

**Red flags**: HTTP calls without timeouts. Immediate retries without backoff (thundering herd).
Using System.currentTimeMillis() for conflict resolution across nodes. Distributed locks
without fencing tokens. Assuming clocks are synchronized across nodes.

---

## 8. Consensus and Coordination

- [ ] Leader election uses a proper consensus protocol (not ad-hoc)
- [ ] Coordination services (ZooKeeper/etcd) used for leader election and configuration
- [ ] No hand-rolled consensus or distributed locking
- [ ] 2PC is avoided for cross-service transactions (use sagas instead)
- [ ] Uniqueness constraints across partitions use linearizable operations

**Red flags**: Home-grown leader election using database timestamps. Two-phase commit across
heterogeneous systems. Distributed lock implemented with Redis SET NX without fencing tokens
or proper expiration handling. Assumption that ZooKeeper watches are instantaneous.

---

## 9. Batch and Stream Processing

- [ ] Batch jobs are idempotent (safe to re-run)
- [ ] Stream consumers are idempotent (safe to replay)
- [ ] Exactly-once semantics achieved via idempotency, not by assumption
- [ ] Processing output goes to a well-defined sink (not side effects scattered in operators)
- [ ] Backpressure mechanism exists (consumers can signal producers to slow down)
- [ ] Checkpointing or microbatching configured for stream fault tolerance
- [ ] Late events / out-of-order events are handled (watermarks, allowed lateness)
- [ ] Window semantics match business requirements (tumbling, hopping, sliding, session)

**Red flags**: Stream consumer that crashes and loses all progress (no checkpointing).
Batch job that partially writes output on failure (not atomic). Producer overwhelming consumer
with no flow control. Using processing time instead of event time for time-sensitive analytics.
No dead letter queue for malformed messages.

---

## 10. Derived Data and Integration

- [ ] Derived data (caches, indexes, views) is maintained via events or CDC — not dual writes
- [ ] Transactional outbox pattern used for reliable event publishing
- [ ] Change Data Capture configured for keeping systems in sync
- [ ] Event schema versioning strategy exists
- [ ] Event consumers can bootstrap from scratch (initial snapshot + streaming)
- [ ] Eventual consistency is acceptable and communicated to users appropriately

**Red flags**: Application code that updates both the primary database and Elasticsearch in
separate calls (dual write — can diverge on failure). No outbox pattern — events published after
transaction commit (can be lost on crash). CDC consumer with no mechanism for initial snapshot.
Derived views that can never be rebuilt from the event log.

---

## 11. Operational Readiness

- [ ] Health check endpoints exist
- [ ] Key metrics exposed: request rate, latency percentiles (p50, p95, p99), error rate
- [ ] Distributed tracing instrumented (OpenTelemetry or equivalent)
- [ ] Structured logging with correlation IDs
- [ ] Alerts configured for critical failure conditions
- [ ] Capacity planning considers tail latency (p99, not just averages)
- [ ] Backpressure and graceful degradation strategies in place
- [ ] Runbooks exist for common failure scenarios

**Red flags**: Only monitoring averages (hides tail latency issues). No distributed tracing
across service boundaries. Console.log as only observability. No runbook for leader failover
or partition rebalancing. No capacity planning for data growth.

---

## Severity Classification

When reporting issues, classify them:

- **Critical**: Data loss risk, correctness issue, or security vulnerability
  (e.g., dual writes without outbox, missing fencing tokens, no transaction isolation for invariants)
- **Major**: Reliability or scalability debt that will cause problems at scale
  (e.g., hot partitions, 2PC across services, no idempotency on retries, wrong storage engine)
- **Minor**: Best practice deviation with limited immediate impact
  (e.g., missing health check, no schema registry, suboptimal compaction settings)
- **Suggestion**: Improvement that would be nice but isn't urgent
  (e.g., consider CQRS for complex queries, evaluate column store for analytics workload)
