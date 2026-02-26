#!/usr/bin/env python3
"""
System Design Interview Doc Generator — Alex Xu 4-step framework.

Usage (one-shot):   python new_design.py "URL Shortener"
Usage (interactive): python new_design.py
"""

import argparse
import math
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Prompting helpers
# ---------------------------------------------------------------------------

def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"{label}{suffix}: ").strip()
        if val:
            return val
        if default:
            return default
        print("  (required)")


def prompt_int(label: str, default: int) -> int:
    while True:
        raw = input(f"{label} [{default:,}]: ").strip()
        if not raw:
            return default
        try:
            return int(raw.replace(",", "").replace("_", ""))
        except ValueError:
            print("  Please enter an integer.")


# ---------------------------------------------------------------------------
# Back-of-envelope calculations
# ---------------------------------------------------------------------------

def human_size(bytes_: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} PB"


def calc_estimations(dau: int, read_write_ratio: int, avg_object_size_bytes: int, years: int) -> dict:
    """Return a dict of derived estimates."""
    total_requests_per_day = dau * read_write_ratio
    write_qps = dau / 86400  # 1 write per user per day assumption
    read_qps = write_qps * read_write_ratio
    peak_qps = read_qps * 2  # common rule of thumb

    writes_per_day = dau  # 1 write per active user
    storage_per_day = writes_per_day * avg_object_size_bytes
    total_storage = storage_per_day * 365 * years

    bandwidth_in = write_qps * avg_object_size_bytes  # bytes/sec
    bandwidth_out = read_qps * avg_object_size_bytes

    return {
        "dau": dau,
        "write_qps": write_qps,
        "read_qps": read_qps,
        "peak_qps": peak_qps,
        "read_write_ratio": read_write_ratio,
        "storage_per_day": storage_per_day,
        "total_storage": total_storage,
        "bandwidth_in": bandwidth_in,
        "bandwidth_out": bandwidth_out,
        "years": years,
        "avg_object_size_bytes": avg_object_size_bytes,
    }


# ---------------------------------------------------------------------------
# Document sections
# ---------------------------------------------------------------------------

def section_requirements(system: str, features: list[str]) -> str:
    func = "\n".join(f"- {f}" for f in features)
    return f"""\
## Step 1: Requirements Clarification

### Functional Requirements
{func}

### Non-Functional Requirements
- High availability: 99.99% uptime (< 52 min downtime/year)
- Low latency: p99 read latency < 100 ms
- Durability: no data loss; replicated across at least 3 availability zones
- Eventual consistency is acceptable for non-critical reads
- The system must be horizontally scalable

### Out of Scope (for this interview)
- Admin dashboard / abuse reporting
- A/B testing infrastructure
- Multi-region write consistency
- Billing / rate-limiting per customer tier (mention but don't design)

### Clarifying Questions to Ask the Interviewer
1. What is the expected scale (DAU, peak QPS)?
2. Read-heavy or write-heavy? What is the read:write ratio?
3. Any latency SLA for writes?
4. Do we need strong consistency or is eventual consistency acceptable?
5. What is the retention period for data?
"""


def section_estimation(e: dict) -> str:
    return f"""\
## Step 2: Back-of-Envelope Estimation

### Assumptions
| Parameter | Value |
|-----------|-------|
| Daily Active Users (DAU) | {e['dau']:,} |
| Read : Write ratio | {e['read_write_ratio']} : 1 |
| Average object size | {human_size(e['avg_object_size_bytes'])} |
| Retention period | {e['years']} years |

### Derived Estimates

**Traffic**
```
Write QPS  = DAU / 86,400 s
           = {e['dau']:,} / 86,400
           ≈ {e['write_qps']:,.1f} writes/sec

Read QPS   = Write QPS × {e['read_write_ratio']}
           ≈ {e['read_qps']:,.0f} reads/sec

Peak QPS   ≈ Read QPS × 2   (rule of thumb)
           ≈ {e['peak_qps']:,.0f} reads/sec
```

**Storage**
```
Storage/day = writes/day × avg object size
            = {e['dau']:,} × {human_size(e['avg_object_size_bytes'])}
            = {human_size(e['storage_per_day'])}

Total       = {human_size(e['storage_per_day'])} × 365 × {e['years']} years
            ≈ {human_size(e['total_storage'])}
```

**Bandwidth**
```
Inbound  ≈ {e['write_qps']:,.1f} req/s × {human_size(e['avg_object_size_bytes'])}
         ≈ {human_size(e['bandwidth_in'])}/s

Outbound ≈ {e['read_qps']:,.0f} req/s × {human_size(e['avg_object_size_bytes'])}
         ≈ {human_size(e['bandwidth_out'])}/s
```

**Cache sizing (80/20 rule)**
```
Hot data = 20% of daily reads × avg object size
         ≈ {human_size(e['read_qps'] * 86400 * 0.20 * e['avg_object_size_bytes'])}
```
"""


def section_high_level(system: str, features: list[str]) -> str:
    return f"""\
## Step 3: High-Level Design

### Component Diagram (describe to interviewer)

```
Clients
  │
  ▼
[CDN / Edge Cache]
  │   (cache hit → return)
  ▼
[Load Balancer]  ←──── health checks
  │
  ├─► [API Server cluster]  (stateless, auto-scaling)
  │         │
  │         ├─► [Cache layer]  (Redis / Memcached)
  │         │         │  cache miss
  │         │         ▼
  │         └─► [Primary DB]  ←── [Read Replicas]
  │
  └─► [Message Queue]  (Kafka / SQS)
            │
            ▼
        [Worker / Consumer]
            │
            ▼
       [Object Storage]  (S3-compatible, for blobs)
```

### Core API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/resource | Create a new resource |
| GET  | /v1/resource/:id | Fetch by ID |
| PUT  | /v1/resource/:id | Update |
| DELETE | /v1/resource/:id | Soft-delete |
| GET  | /v1/healthz | Health check |

### Data Model (core entities)

```sql
-- Primary entity
CREATE TABLE resource (
    id          CHAR(8)       PRIMARY KEY,   -- or UUID
    owner_id    BIGINT        NOT NULL,
    payload     TEXT,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    is_deleted  BOOLEAN       NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_resource_owner ON resource(owner_id);
```

### Technology Choices
| Layer | Choice | Rationale |
|-------|--------|-----------|
| API | REST / gRPC | REST for external; gRPC for internal services |
| Primary DB | PostgreSQL (or Cassandra if write-heavy) | ACID; mature; read replicas |
| Cache | Redis | Sub-millisecond latency; rich data structures |
| Object store | S3-compatible | Cheap; durable; decoupled from DB |
| Queue | Kafka | High-throughput; replay; partitioned by key |
"""


def section_deep_dive(system: str, e: dict) -> str:
    return f"""\
## Step 4: Deep Dive

### Bottleneck Analysis
- **Write path**: API server → DB primary. Mitigate with write-ahead log tailing,
  async replication, and buffered writes via the message queue.
- **Read path**: DB read replicas + Redis cache. Target > 90% cache hit rate.
- **Hot keys**: Apply key-based sharding and local in-process LRU cache for the
  top-N items (identified via cache hit analytics).

### Database Deep Dive

**Why {("Cassandra" if e["write_qps"] > 5000 else "PostgreSQL")}?**
{"Cassandra: wide-column store optimised for high write throughput with tunable consistency. Partition key = user_id for even distribution." if e["write_qps"] > 5000 else "PostgreSQL: strong ACID guarantees, mature tooling, easy to add read replicas. Move to Cassandra if write QPS exceeds ~10k sustained."}

**Sharding strategy**
- Shard by `user_id` hash to distribute load evenly.
- Avoid sharding by time (creates hot partitions for recent data).
- Use consistent hashing to minimise re-sharding cost.

**Replication**
- 1 primary + 2 read replicas per shard (cross-AZ).
- Async replication is acceptable; compensate with cache TTL.

### Caching Strategy
- **Read-through cache**: API checks Redis before DB.
- **Write-invalidation**: On write, delete the cache key (not update).
- **TTL**: Set based on staleness tolerance (e.g., 5 min for non-critical data).
- **Eviction policy**: `allkeys-lru` for general use.

### Consistency Model
- Reads from replicas may be slightly stale (< 1 s typical).
- Critical reads (e.g., immediately after a write) can be routed to primary.
- Use optimistic locking (version column) for concurrent updates.

### Fault Tolerance
- API servers: stateless → replace failed nodes automatically.
- DB primary failure: automated failover to replica (< 30 s with Patroni/RDS).
- Cache failure: graceful degradation — fall through to DB.
- Queue failure: producers buffer locally and retry.

### Scalability Levers (ordered by cost)
1. Increase read replica count.
2. Add Redis cluster nodes.
3. Add API server instances (auto-scaling policy on CPU/QPS).
4. Shard the database.
5. Move to a distributed DB (Cassandra / CockroachDB).

### Areas to Explore If Time Permits
- **CDN**: Cache static and semi-static responses at edge.
- **Rate limiting**: Token bucket per user_id at the load balancer.
- **Search**: Add Elasticsearch for full-text queries.
- **Analytics**: Stream events to a data warehouse (Snowflake / BigQuery) via Kafka.
"""


def section_interview_questions(system: str) -> str:
    return f"""\
## Common Follow-Up Interview Questions

| Question | Key Points to Cover |
|----------|---------------------|
| How do you handle a DB primary failure? | Automated failover, replica promotion, heartbeat checks |
| How do you prevent cache stampede? | Mutex lock on cache miss, probabilistic early refresh |
| How would you design the ID generation? | Snowflake ID, UUID v7, or DB sequence — trade-offs |
| How do you ensure exactly-once processing? | Idempotency keys, deduplication in the consumer |
| How would you add full-text search? | Elasticsearch / OpenSearch, sync via CDC from DB |
| How do you handle schema migrations? | Expand/contract pattern; blue/green deploys; backward-compatible changes first |
| Walk me through a write from client to storage | Client → LB → API → validate → DB write → publish event → async worker |
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def gather_interactive() -> dict:
    print("\n=== System Design Interview — Document Generator ===\n")
    system = prompt("System name (e.g., 'URL Shortener', 'Twitter Feed')")
    features_raw = prompt(
        "Core features (comma-separated)",
        "Create resource, Retrieve resource, Delete resource"
    )
    features = [f.strip() for f in features_raw.split(",") if f.strip()]
    dau = prompt_int("DAU (Daily Active Users)", 10_000_000)
    rw = prompt_int("Read:Write ratio (e.g., 10 means 10 reads per write)", 10)
    obj_size = prompt_int("Average object size in bytes", 1024)
    years = prompt_int("Retention period (years)", 5)
    output_raw = prompt("Output file (leave blank for stdout)", "")
    output = Path(output_raw) if output_raw else None
    return dict(system=system, features=features, dau=dau, rw=rw,
                obj_size=obj_size, years=years, output=output)


def render(data: dict) -> str:
    system = data["system"]
    e = calc_estimations(
        dau=data["dau"],
        read_write_ratio=data["rw"],
        avg_object_size_bytes=data["obj_size"],
        years=data["years"],
    )
    parts = [
        f"# System Design: {system}",
        "",
        f"**Date:** {date.today()}  ",
        f"**Framework:** Alex Xu — System Design Interview Vol. 1 & 2",
        "",
        "---",
        "",
        section_requirements(system, data["features"]),
        "---",
        "",
        section_estimation(e),
        "---",
        "",
        section_high_level(system, data["features"]),
        "---",
        "",
        section_deep_dive(system, e),
        "---",
        "",
        section_interview_questions(system),
        "---",
        "",
        "*Generated by `new_design.py` — System Design Interview skill.*",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a system design interview document (Alex Xu framework)."
    )
    parser.add_argument("system", nargs="?", help="System name (skips prompt if provided)")
    parser.add_argument("--dau", type=int, default=None)
    parser.add_argument("--rw", type=int, default=None, help="Read:write ratio")
    parser.add_argument("--obj-size", type=int, default=None, help="Avg object size in bytes")
    parser.add_argument("--years", type=int, default=None, help="Retention years")
    parser.add_argument("--features", help="Comma-separated feature list")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if args.system and args.dau and args.rw and args.obj_size and args.years:
        features = (
            [f.strip() for f in args.features.split(",")]
            if args.features
            else ["Create resource", "Read resource", "Delete resource"]
        )
        data = dict(
            system=args.system, features=features,
            dau=args.dau, rw=args.rw,
            obj_size=args.obj_size, years=args.years,
            output=args.output,
        )
    else:
        if args.system:
            # System name given but other params missing — use defaults
            data = dict(
                system=args.system,
                features=["Create resource", "Read resource", "Delete resource"],
                dau=10_000_000, rw=10, obj_size=1024, years=5,
                output=args.output,
            )
        else:
            try:
                data = gather_interactive()
            except (KeyboardInterrupt, EOFError):
                print("\nAborted.", file=sys.stderr)
                sys.exit(1)

    document = render(data)

    if data.get("output"):
        data["output"].write_text(document)
        print(f"Design document written to: {data['output']}")
    else:
        sys.stdout.write(document)


if __name__ == "__main__":
    main()
