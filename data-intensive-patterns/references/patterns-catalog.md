# Data-Intensive Application Patterns Catalog

Comprehensive reference of patterns from Martin Kleppmann's *Designing Data-Intensive Applications*.
Organized by the book's three-part structure. Read the section relevant to the code you're generating.

---

## Table of Contents

1. [Data Models and Query Languages](#data-models-and-query-languages)
2. [Storage Engines and Indexing](#storage-engines-and-indexing)
3. [Encoding and Schema Evolution](#encoding-and-schema-evolution)
4. [Replication](#replication)
5. [Partitioning](#partitioning)
6. [Transactions](#transactions)
7. [Distributed Systems Fundamentals](#distributed-systems-fundamentals)
8. [Consistency and Consensus](#consistency-and-consensus)
9. [Batch Processing](#batch-processing)
10. [Stream Processing](#stream-processing)
11. [Derived Data and Integration](#derived-data-and-integration)

---

## Data Models and Query Languages

### Relational Model
- Tables with rows and columns, enforced schema
- Best for: many-to-many relationships, complex joins, data with strong integrity requirements
- Normalized: reduce redundancy, enforce consistency via foreign keys
- Query language: SQL (declarative)

### Document Model
- Self-contained JSON/BSON documents, flexible schema (schema-on-read)
- Best for: one-to-many relationships, self-contained records, heterogeneous data
- Denormalized: data locality — everything for one entity in one document
- Limitations: poor support for many-to-many; joins are weak or manual
- Examples: MongoDB, CouchDB, RethinkDB

### Graph Model
- Vertices (nodes) and edges (relationships), flexible schema
- Best for: highly interconnected data, variable relationship types, traversal-heavy queries
- Two flavors:
  - **Property graph** (Neo4j): nodes/edges have properties, query with Cypher
  - **Triple store** (RDF): subject-predicate-object triples, query with SPARQL
- Good for social networks, recommendation engines, knowledge graphs, fraud detection

### Choosing a Data Model

| Access Pattern | Best Model |
|---------------|-----------|
| Complex joins, aggregations, reporting | Relational |
| Self-contained documents, flexible schema | Document |
| Highly connected data, graph traversals | Graph |
| Append-only event log | Event store |
| Key-value lookups with high throughput | Key-value (Redis, DynamoDB) |
| Time-series with range scans | Time-series (TimescaleDB, InfluxDB) |

---

## Storage Engines and Indexing

### Log-Structured Storage (LSM-Trees)

How it works:
1. Writes go to an in-memory balanced tree (memtable)
2. When memtable exceeds threshold, flush to disk as a sorted SSTable (Sorted String Table)
3. Background compaction merges SSTables, removing duplicates and deleted entries
4. Reads check memtable first, then SSTables (newest to oldest), aided by Bloom filters

Characteristics:
- **Write-optimized**: sequential writes to disk, no random I/O on write path
- **Compaction strategies**: size-tiered (good for write-heavy) vs leveled (better read amplification)
- **Bloom filters**: probabilistic data structure to quickly check if a key might exist in an SSTable
- **Trade-off**: higher write throughput, but reads may touch multiple SSTables

Implementations: LevelDB, RocksDB, Cassandra, HBase, ScyllaDB

### Page-Oriented Storage (B-Trees)

How it works:
1. Data organized in fixed-size pages (typically 4KB)
2. Tree structure with branching factor ~several hundred
3. Updates modify pages in place
4. Write-ahead log (WAL) ensures crash recovery

Characteristics:
- **Read-optimized**: O(log n) lookups with predictable performance
- **In-place updates**: overwrites pages on disk
- **WAL**: append-only log written before modifying pages, for crash recovery
- **Latches**: lightweight locks for concurrent access to tree pages
- **Copy-on-write**: some implementations (LMDB) write new pages instead of overwriting

Implementations: PostgreSQL, MySQL InnoDB, SQL Server, Oracle

### Choosing a Storage Engine

| Workload | Recommended Engine | Why |
|----------|-------------------|-----|
| Write-heavy (logging, IoT, events) | LSM-Tree | Sequential writes, high throughput |
| Read-heavy with point lookups | B-Tree | Predictable read latency |
| Mixed OLTP | B-Tree (usually) | Good all-around for transactions |
| Analytical (OLAP) | Column-oriented | Compression, vectorized processing |
| Time-series | LSM-Tree or specialized | Append-heavy, range scan friendly |

### Column-Oriented Storage (OLAP)

- Store values from each column together instead of each row together
- Enables aggressive compression (run-length encoding, bitmap encoding)
- Vectorized processing: operate on columns of compressed data in CPU cache
- **Star schema**: central fact table with dimension tables (snowflake if dimensions are further normalized)
- **Materialized views / data cubes**: pre-computed aggregations for dashboard queries

---

## Encoding and Schema Evolution

### Encoding Formats Comparison

| Format | Schema? | Binary? | Forward Compatible | Backward Compatible | Notes |
|--------|---------|---------|-------------------|--------------------|----|
| JSON | Optional (JSON Schema) | No | Partial | Partial | Human-readable; number precision issues |
| XML | Optional (XSD) | No | Partial | Partial | Verbose; human-readable |
| Protocol Buffers | Required (.proto) | Yes | Yes (new fields with new tags) | Yes (new fields optional) | Field tags for evolution |
| Thrift | Required (.thrift) | Yes | Yes | Yes | Similar to Protobuf, two binary formats |
| Avro | Required (.avsc) | Yes | Yes (writer's schema + reader's schema) | Yes | Schema resolution; great for Hadoop/Kafka |

### Schema Evolution Rules

- **Forward compatibility**: old code can read data written by new code
  - New fields must be optional or have defaults
  - Never remove a required field
- **Backward compatibility**: new code can read data written by old code
  - New fields must be optional or have defaults
  - Never reuse a deleted field's tag number
- **Full compatibility** (both): needed when readers and writers are updated at different times

### Dataflow Patterns

How data flows between processes determines which compatibility direction matters:

- **Through databases**: writer encodes, reader decodes (potentially much later) — need both directions
- **Through services (REST/RPC)**: request and response each need backward + forward compatibility
  - REST: use content negotiation, versioned URLs, or header-based versioning
  - RPC: treat as cross-service API, version carefully
- **Through async messaging**: producer encodes, consumer decodes — similar to databases
  - Use schema registry (Confluent Schema Registry for Kafka)
  - Avro is ideal: writer's schema stored with each message, reader uses its own schema

---

## Replication

### Single-Leader Replication

One node (leader) accepts writes; followers replicate the leader's write-ahead log.

- **Synchronous followers**: guaranteed up-to-date but write latency increases
- **Asynchronous followers**: leader doesn't wait, risk of data loss if leader fails before replication
- **Semi-synchronous**: one follower is synchronous (guaranteed durability), rest are async

Failover concerns:
- Split-brain: two nodes think they're leader (use fencing tokens, epoch numbers)
- Lost writes: async follower promoted to leader may be missing recent writes
- Replication lag: stale reads from followers

Handling replication lag:
- **Read-after-write consistency**: after a write, read from leader (or wait for follower to catch up)
- **Monotonic reads**: always read from the same replica (session stickiness)
- **Consistent prefix reads**: preserve causal ordering of writes

### Multi-Leader Replication

Multiple nodes accept writes. Each leader replicates to all others.

- **Use case**: multi-datacenter (one leader per datacenter), offline-capable clients, collaborative editing
- **Conflict resolution**:
  - Last-write-wins (LWW): discard concurrent writes arbitrarily — data loss risk
  - Merge values: application-specific merge logic
  - Custom conflict handlers: on-write or on-read resolution
- **Topologies**: all-to-all (best), star, circular (avoid single points of failure)

### Leaderless Replication (Dynamo-style)

Client sends writes to multiple replicas. Reads query multiple replicas.

- **Quorum**: w + r > n (write quorum + read quorum > total replicas) to guarantee overlap
  - Common config: n=3, w=2, r=2
  - Tunable: w=1, r=3 for fast writes; w=3, r=1 for fast reads
- **Read repair**: client detects stale value during read, writes newer value back to stale replica
- **Anti-entropy**: background process compares replicas and fixes differences
- **Sloppy quorum + hinted handoff**: during network partition, write to reachable nodes, hand off later
- **Version vectors**: track causal history to detect concurrent writes vs. sequential

---

## Partitioning

### Partitioning Strategies

**By key range:**
- Keys sorted, each partition owns a contiguous range
- Enables efficient range scans
- Risk: hot spots if writes cluster on one range (e.g., time-based keys → today's partition is hot)
- Mitigation: compound keys (e.g., sensor_id + timestamp)

**By hash of key:**
- Hash function distributes keys uniformly across partitions
- Destroys sort order — range scans require querying all partitions
- More uniform load distribution
- Consistent hashing: minimizes data movement when adding/removing nodes

**Compound/composite partitioning:**
- First part of key determines partition (by hash), rest preserves sort order within partition
- Cassandra approach: partition key (hashed) + clustering columns (sorted within partition)

### Secondary Indexes with Partitioning

**Document-partitioned (local) index:**
- Each partition maintains its own secondary index covering only its data
- Write: update one partition's index
- Read: scatter-gather across all partitions (fan-out) — can be slow

**Term-partitioned (global) index:**
- Secondary index is itself partitioned by the indexed term
- Write: may need to update multiple partitions' indexes (distributed transaction or async)
- Read: query only the relevant index partition — faster reads

### Rebalancing Strategies

- **Fixed number of partitions**: create many more partitions than nodes; reassign whole partitions when nodes join/leave (Riak, Elasticsearch, Couchbase)
- **Dynamic partitioning**: split large partitions, merge small ones (HBase, RethinkDB)
- **Proportional to nodes**: fixed number of partitions per node (Cassandra)
- **Avoid**: hash mod N (reassigns almost everything when N changes)

### Request Routing

- **Client-side**: client learns partition assignment (via ZooKeeper/gossip) and connects directly
- **Routing tier**: proxy/load balancer that knows partition assignment
- **Coordinator node**: any node accepts request, forwards to correct partition owner (Cassandra gossip)

---

## Transactions

### Isolation Levels

**Read Committed:**
- Guarantees: no dirty reads (only see committed data), no dirty writes (only overwrite committed data)
- Implementation: row-level locks for writes; snapshot for reads (return old committed value during write)
- Default in PostgreSQL, SQL Server

**Snapshot Isolation (Repeatable Read / MVCC):**
- Each transaction sees a consistent snapshot of the database from the start of the transaction
- Implementation: MVCC (Multi-Version Concurrency Control) — each write creates a new version; reads see only versions committed before the transaction started
- Prevents: read skew (non-repeatable reads)
- Does NOT prevent: write skew (two transactions read, then both write based on stale reads)

**Serializable:**
- Strongest guarantee — result is as if transactions ran one-at-a-time

Three implementations:
1. **Actual serial execution**: literally run one transaction at a time on a single CPU
   - Viable when transactions are short and fit in memory
   - Use stored procedures to avoid network round-trips
   - Partitioning can enable per-partition serial execution
2. **Two-phase locking (2PL)**: readers block writers, writers block readers
   - Shared locks for reads, exclusive locks for writes
   - Predicate locks or index-range locks prevent phantoms
   - Performance: significant contention, potential deadlocks
3. **Serializable Snapshot Isolation (SSI)**: optimistic — detect conflicts at commit time
   - Based on snapshot isolation + tracking reads and writes
   - Detect: writes that affect prior reads (stale MVCC reads)
   - Abort conflicting transactions at commit
   - Better performance than 2PL for low-contention workloads

### Preventing Write Skew and Phantoms

Write skew: two transactions both read a condition, both decide to act, both write — violating a constraint that should hold across both.

Example: two doctors both check "≥2 doctors on call" → both remove themselves → 0 on call.

Solutions:
- Serializable isolation
- Explicit locking: `SELECT ... FOR UPDATE` to materialize the conflict
- Application-level constraints with saga patterns

Phantoms: a write in one transaction changes the result of a search query in another.

Solutions:
- Predicate locks (lock the search condition itself)
- Index-range locks (practical approximation of predicate locks)
- Materializing conflicts: create a lock table that represents the condition

---

## Distributed Systems Fundamentals

### Unreliable Networks

- Networks are **asynchronous**: no upper bound on message delay
- Packet loss, reordering, duplication are normal
- **Timeout selection**: too short → false positives (unnecessary failover); too long → slow detection
  - Adaptive timeouts based on observed round-trip times
- **Network partitions**: some nodes can't communicate with others

### Unreliable Clocks

- **Time-of-day clocks**: wall clock, can jump (NTP sync, leap seconds) — DO NOT use for durations or ordering
- **Monotonic clocks**: always move forward, for measuring elapsed time within a single node
- **Logical clocks**: Lamport timestamps, vector clocks — capture causal ordering without relying on physical time

Clock issues in distributed systems:
- LWW conflict resolution using timestamps is fundamentally unsafe
- Lease expiration: a process might think its lease is valid when the clock has drifted
- Solution: **fencing tokens** — monotonically increasing tokens; storage rejects stale tokens

### Process Pauses

- GC pauses, VM suspension, disk I/O stalls can freeze a process for seconds
- A process cannot know it was paused — it might act on stale state after resuming
- Solution: lease-based protocols with fencing tokens; always validate at the point of write

### Fencing Tokens

When using distributed locks or leases:
1. Lock service issues a fencing token (monotonically increasing number) with each lock grant
2. Client includes fencing token with every write to the storage service
3. Storage service rejects writes with a token lower than the highest seen
4. Guarantees mutual exclusion even if a client holds a stale lock

---

## Consistency and Consensus

### Linearizability

Strongest consistency model: operations appear to take effect atomically at some point between invocation and completion. Like a single-copy system.

- **Use cases**: leader election, uniqueness constraints, distributed locks
- **Not needed for**: most application reads, analytics, caching
- **Cost**: slower (requires coordination), reduced availability during network partitions

CAP Theorem (more precisely): if there's a network partition, you must choose between consistency (linearizability) and availability.

### Causal Consistency

Weaker than linearizability but preserves causally related ordering:
- If operation A happened before B, everyone sees A before B
- Concurrent operations can be seen in different orders by different nodes
- Implemented via: version vectors, Lamport timestamps

### Total Order Broadcast

Protocol to deliver messages to all nodes in the same order:
- All nodes deliver the same messages in the same sequence
- Equivalent to consensus (and to linearizable compare-and-swap)
- Implementations: ZooKeeper's Zab, Raft's log replication

### Distributed Consensus

Agreement: all nodes decide on the same value. Properties:
- **Uniform agreement**: no two nodes decide differently
- **Integrity**: a node decides at most once
- **Validity**: if a node decides value v, then v was proposed by some node
- **Termination**: every non-crashed node eventually decides

Algorithms: Paxos, Raft, Zab (ZooKeeper), Viewstamped Replication

Practical usage: don't implement consensus yourself. Use:
- **ZooKeeper/etcd**: coordination services providing linearizable key-value store, leader election, distributed locks, group membership, service discovery
- **Raft-based systems**: etcd (Kubernetes), CockroachDB, TiKV

### Two-Phase Commit (2PC) — and Why to Avoid It

Coordinator-based distributed transaction protocol:
1. Prepare phase: coordinator asks all participants to prepare (vote yes/no)
2. Commit phase: if all vote yes, coordinator commits; if any vote no, abort

Problems:
- **Blocking**: if coordinator crashes after prepare, participants are stuck holding locks
- **Single point of failure**: coordinator must be highly available
- **Performance**: high latency, reduced throughput due to lock holding
- **Heterogeneous systems**: XA transactions across different databases are especially fragile

Prefer: sagas with compensating transactions, or single-database transactions with outbox pattern.

---

## Batch Processing

### Unix Philosophy Applied to Data

- Small, focused tools composed via pipes
- Immutable inputs, explicit outputs
- Separate the logic from the wiring

### MapReduce

How it works:
1. **Map**: extract key-value pairs from each input record
2. **Shuffle**: group all values for the same key together (sorted)
3. **Reduce**: process all values for each key, produce output

Patterns:
- **Sort-merge join (reduce-side)**: both datasets emit the join key; reducer sees all matching records
- **Broadcast hash join (map-side)**: small dataset loaded into memory in each mapper; no shuffle needed
- **Partitioned hash join (map-side)**: both datasets partitioned the same way; each mapper joins its own partition pair

Limitations of MapReduce:
- Materializes intermediate state to disk between stages (slow)
- Overhead of repeated job startup

### Dataflow Engines (Spark, Flink, Tez)

Improvements over MapReduce:
- Model entire workflow as a directed acyclic graph (DAG) of operators
- No mandatory materialization of intermediate results (can pipeline through memory)
- Operators are generalized (not limited to map and reduce)
- Better fault tolerance: recompute from upstream operator or checkpoint

### Graph Processing (Pregel / BSP)

Bulk Synchronous Parallel model for iterative graph algorithms:
- Each vertex processes messages from its neighbors
- Sends messages to neighbors for the next iteration
- Iterations continue until convergence (no more messages)
- Use for: PageRank, shortest paths, connected components

---

## Stream Processing

### Message Brokers vs. Log-Based Systems

**Traditional message broker** (RabbitMQ, ActiveMQ):
- Messages deleted after acknowledgment
- No long-term history
- Multiple consumers: load balancing (competing consumers) or fan-out (pub/sub)
- Good for: task queues, work distribution

**Log-based message broker** (Kafka, Amazon Kinesis):
- Append-only log, messages retained for configurable period
- Consumers track their position (offset) in the log
- Multiple consumer groups read independently at their own pace
- Replay: reset offset to re-process past messages
- Ordering guaranteed within a partition

### Change Data Capture (CDC)

Capture every write to a database and publish it as an event stream:
- **Implementation**: read the database's replication log (WAL) and convert to events
- **Tools**: Debezium (Kafka Connect), Maxwell, AWS DMS
- **Initial snapshot**: bootstrap new consumer with a full table dump, then switch to streaming
- **Log compaction**: retain only the latest event for each key — bounded storage, full state rebuild

Use CDC to keep derived systems (search indexes, caches, data warehouses) in sync with the primary database.

### Event Sourcing

Store every state change as an immutable event in an append-only log:
- Current state = replay all events from the beginning (or from a snapshot)
- Events are facts — never deleted or modified
- Commands (requests) are validated and may be rejected; events (facts) are always recorded
- **Snapshots**: periodically save materialized state to avoid replaying entire history

Differences from CDC:
- CDC captures low-level database changes (row inserts/updates/deletes)
- Event sourcing captures high-level domain events (OrderPlaced, PaymentReceived)
- Event sourcing is designed into the application; CDC is applied to existing databases

### Stream Processing Patterns

**Complex Event Processing (CEP):**
- Define patterns over event streams (e.g., "three failed logins within 5 minutes")
- Query is stored, events flow through the query
- Tools: Esper, Apache Flink CEP

**Stream analytics:**
- Continuous aggregation over time windows
- Window types:
  - **Tumbling**: fixed-size, non-overlapping (e.g., every 1 minute)
  - **Hopping**: fixed-size, overlapping (e.g., 5-min window every 1 min)
  - **Sliding**: all events within a fixed duration of each other
  - **Session**: group events by activity with inactivity gap

**Stream joins:**
- **Stream-stream join (window join)**: join two streams within a time window; buffer events from both sides
- **Stream-table join (enrichment)**: enrich stream events with data from a table (maintained locally via CDC or changelog)
- **Table-table join (materialized view)**: both inputs are changelogs; output is an updated materialized view

### Stream Fault Tolerance

- **Microbatching** (Spark Streaming): process stream in small batches; replay batch on failure
- **Checkpointing** (Flink): periodic snapshots of operator state; restore from last checkpoint
- **Idempotent writes**: make sink operations idempotent so replayed messages don't cause duplicates
- **Exactly-once semantics**: achieved via atomic commit of state + output + offset (Kafka transactions), or idempotency keys at the sink
- **Rebuilding state**: if a local state store is lost, rebuild from the changelog or re-process the input stream

---

## Derived Data and Integration

### The Dataflow Paradigm

Think of data systems as a pipeline:
- **System of record** (source of truth): authoritative data store
- **Derived data**: caches, search indexes, materialized views, data warehouse — all derived from the source of truth
- A change to the source of truth triggers updates to all derived views

### Transactional Outbox Pattern

Ensure reliable event publishing alongside database writes:
1. Write business data AND event to an OUTBOX table in the same database transaction
2. A separate process (relay) reads the outbox and publishes events to the message broker
3. After successful publish, mark outbox entry as published

Relay strategies:
- **Polling publisher**: periodically query the outbox table for unpublished events
- **Transaction log tailing**: read the database's WAL to detect outbox inserts (lower latency)

### CQRS (Command Query Responsibility Segregation)

Separate the write model from the read model:
- **Command side**: handles writes, publishes domain events
- **Query side**: subscribes to events, maintains denormalized read-optimized views

Benefits:
- Read model optimized for specific query patterns
- Read and write sides can scale independently
- Can have multiple read models for different access patterns

Trade-offs:
- Eventual consistency between write and read sides
- More infrastructure (event bus, separate read databases)
- Complexity of maintaining derived views

### Lambda Architecture vs. Kappa Architecture

**Lambda**: maintain both a batch layer (reprocess all data periodically) and a speed layer (process new events in real time); merge results.
- Problem: maintaining two codepaths (batch and streaming)

**Kappa**: single stream processing system handles everything; reprocess by replaying the log from the beginning through a new version of the processor.
- Simpler; requires log retention and ability to replay

### End-to-End Correctness

No single component provides exactly-once across the entire pipeline. Instead:
- Use **idempotency keys** at every boundary (producer → broker → consumer → database)
- **Deduplication**: consumers track processed message IDs
- **End-to-end argument**: push correctness guarantees to the application level rather than relying on infrastructure
- **Deterministic processing**: same input always produces same output, enabling safe replay
