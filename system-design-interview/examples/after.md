# After

A structured URL shortener design that follows the 4-step framework: scope clarification, back-of-envelope estimation, high-level component design, and a focused deep dive.

```
DESIGN: URL Shortener Service

─────────────────────────────────────────────────────────────
STEP 1 — SCOPE & REQUIREMENTS
─────────────────────────────────────────────────────────────
Functional requirements:
  - POST /shorten          → create short URL, return 7-char code
  - GET  /{code}           → redirect to original URL (301 or 302)
  - Custom aliases         → optional
  - Expiration             → optional TTL per URL

Non-functional requirements:
  - 100M URLs shortened per day
  - Read:Write ratio ~ 100:1 (redirects far outnumber shortens)
  - 99.9% availability for redirects (latency < 50ms p99)
  - URLs persist indefinitely (unless TTL set)

─────────────────────────────────────────────────────────────
STEP 2 — BACK-OF-ENVELOPE ESTIMATION
─────────────────────────────────────────────────────────────
Write QPS:  100M / 86,400 sec ≈ 1,160 writes/sec
Read QPS:   100:1 ratio       ≈ 116,000 reads/sec

Storage (10-year horizon):
  100M writes/day × 365 × 10 = 365B URLs
  Each record ≈ 500 bytes
  Total ≈ 365B × 500B ≈ 182 TB

Cache:
  80/20 rule: 20% of URLs serve 80% of traffic
  Hot URLs: 116,000 reads/sec × 0.2 × 500B ≈ ~12 MB/sec cache traffic
  In-memory cache size: 1M hot entries × 500B ≈ 500 MB (fits on one Redis node)

─────────────────────────────────────────────────────────────
STEP 3 — HIGH-LEVEL DESIGN
─────────────────────────────────────────────────────────────

[Client]
   │
   ▼
[CDN / Load Balancer]
   │
   ├──> [Redirect Service]  ──cache hit──>  [Redis Cache (hot URLs)]
   │         │                                       │ cache miss
   │         └─────────────────────────────> [URL DB read replica]
   │
   └──> [Shortening Service]
              │
              ├──> [ID Generator Service]  (Twitter Snowflake: 64-bit IDs
              │                             → Base62 encodes to 7 chars)
              │
              └──> [URL DB primary - MySQL]  ─replication─>  [Read Replicas]

API contract:
  POST /api/v1/shorten
    Body: { "longUrl": "https://...", "ttl": 86400 }
    Response: { "shortUrl": "https://short.ly/aB3xY2k" }

  GET /aB3xY2k
    Response: HTTP 301 (permanent, browser caches) or 302 (temporary, server tracks clicks)

─────────────────────────────────────────────────────────────
STEP 4 — DEEP DIVE: ID Generation
─────────────────────────────────────────────────────────────
Problem: UUID first-8-chars has high collision probability at scale.

Solution: Twitter Snowflake-style 64-bit ID:
  [41-bit timestamp ms] + [10-bit machine ID] + [12-bit sequence]
  → Globally unique, monotonically increasing, no coordination needed
  → Base62 encode (a-z, A-Z, 0-9): 7 chars covers 62^7 ≈ 3.5 trillion URLs

Collision handling: none needed — IDs are guaranteed unique by construction.

─────────────────────────────────────────────────────────────
OPERATIONAL CONCERNS
─────────────────────────────────────────────────────────────
- Cache eviction: LRU, 24-hour TTL for hot entries
- DB sharding: shard by short_code hash when single primary exceeds 10TB
- Rate limiting: 100 shortens/hour per IP via token bucket
- Monitoring: p99 redirect latency, cache hit rate, DB replication lag
```

Key improvements:
- Back-of-envelope estimation (116K reads/sec, 182TB, 500MB cache) validates that a single Redis node suffices and that DB sharding is a future concern, not a day-one requirement (Ch 2: Estimation before design)
- The 4-step framework structures the proposal — scope before design, estimation before components, component overview before deep dive (Ch 3: 4-step framework)
- API contract is defined explicitly before implementation — POST/GET endpoints with request/response shapes (Ch 3: High-level design)
- Snowflake ID generation replaces UUID truncation with a correct solution: no collisions at 100M/day scale (Ch 7: Unique ID generation)
- Read replicas serve the 100:1 read-heavy workload; Redis caches the hot 20% to keep redirect latency under 50ms (Ch 1: Caching and replication)
- 301 vs 302 redirect choice is a conscious trade-off: 301 reduces server load, 302 enables analytics — stated explicitly (Ch 8: URL Shortener)
