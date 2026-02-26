# System Design Interview — Design Review Checklist

Systematic checklist for reviewing system designs against the 16 chapters
from *System Design Interview* by Alex Xu.

---

## 1. Scaling Fundamentals (Chapter 1)

### Infrastructure
- [ ] **Ch 1 — Load balancing** — Is traffic distributed across multiple servers with failover?
- [ ] **Ch 1 — Database replication** — Are read replicas used for read-heavy workloads?
- [ ] **Ch 1 — Caching** — Is a cache layer (Redis/Memcached) used for frequently accessed data?
- [ ] **Ch 1 — CDN** — Are static assets served from a CDN?
- [ ] **Ch 1 — Stateless web tier** — Is session data stored in shared storage, not on web servers?
- [ ] **Ch 1 — Message queue** — Are time-consuming tasks decoupled via async message queues?
- [ ] **Ch 1 — Database sharding** — Is data sharded for write-heavy or large-scale workloads?
- [ ] **Ch 1 — Data centers** — Is multi-datacenter deployment considered for geo-distribution?

### Data Layer
- [ ] **Ch 1 — Database choice** — Is the right database type selected (SQL vs. NoSQL) based on access patterns?
- [ ] **Ch 1 — Shard key** — Is the shard key chosen for even data distribution?
- [ ] **Ch 1 — Hotspot mitigation** — Are celebrity/hotspot problems addressed?

---

## 2. Capacity Estimation (Chapter 2)

### Back-of-Envelope
- [ ] **Ch 2 — QPS estimated** — Are queries per second calculated (average and peak)?
- [ ] **Ch 2 — Storage estimated** — Is storage growth estimated over time (1 year, 5 years)?
- [ ] **Ch 2 — Bandwidth estimated** — Is network bandwidth estimated for read and write?
- [ ] **Ch 2 — Memory estimated** — Is cache memory estimated (e.g., 80/20 rule)?
- [ ] **Ch 2 — Availability target** — Is the availability SLA defined (99.9%, 99.99%)?
- [ ] **Ch 2 — Latency awareness** — Are latency numbers considered (memory vs. disk vs. network)?

---

## 3. Design Structure (Chapter 3)

### Framework Adherence
- [ ] **Ch 3 — Requirements defined** — Are functional and non-functional requirements explicit?
- [ ] **Ch 3 — High-level design** — Is there a clear component diagram with data flow?
- [ ] **Ch 3 — API design** — Are API endpoints defined?
- [ ] **Ch 3 — Deep dive** — Are 2–3 critical components designed in detail?
- [ ] **Ch 3 — Trade-offs stated** — Are design trade-offs explicitly discussed?
- [ ] **Ch 3 — Error handling** — Are failure modes and error handling addressed?
- [ ] **Ch 3 — Monitoring** — Is logging, metrics, and alerting included?

---

## 4. Rate Limiting (Chapter 4)

### Rate Limiter Design
- [ ] **Ch 4 — Algorithm selected** — Is an appropriate rate limiting algorithm chosen for the use case?
- [ ] **Ch 4 — Distributed concerns** — Are race conditions and multi-server sync addressed?
- [ ] **Ch 4 — Rate limit response** — Are proper HTTP 429 responses and headers used?
- [ ] **Ch 4 — Rule configuration** — Are rate limiting rules configurable and cached?

---

## 5. Data Distribution (Chapter 5)

### Consistent Hashing
- [ ] **Ch 5 — Hash strategy** — Is consistent hashing used for data/request distribution?
- [ ] **Ch 5 — Virtual nodes** — Are virtual nodes used for even distribution?
- [ ] **Ch 5 — Rebalancing** — Is key redistribution minimized when servers change?

---

## 6. Distributed Storage (Chapter 6)

### Key-Value Store Design
- [ ] **Ch 6 — CAP choice** — Is the CP vs. AP trade-off explicitly decided?
- [ ] **Ch 6 — Replication** — Is data replicated to N nodes with appropriate quorum (N/W/R)?
- [ ] **Ch 6 — Conflict resolution** — Are concurrent write conflicts handled (vector clocks, last-write-wins)?
- [ ] **Ch 6 — Failure detection** — Is gossip protocol or equivalent used for failure detection?
- [ ] **Ch 6 — Failure recovery** — Are sloppy quorum and hinted handoff used for temporary failures?
- [ ] **Ch 6 — Anti-entropy** — Are Merkle trees used for replica synchronization?

---

## 7. Unique IDs (Chapter 7)

### ID Generation
- [ ] **Ch 7 — ID approach** — Is the right ID generation approach used for the requirements?
- [ ] **Ch 7 — Sortability** — Are IDs sortable by time if needed (snowflake)?
- [ ] **Ch 7 — Distribution** — Can IDs be generated without central coordination?
- [ ] **Ch 7 — Size** — Is the ID size appropriate (64-bit vs. 128-bit)?

---

## 8. URL Shortening (Chapter 8)

### URL Shortener Design
- [ ] **Ch 8 — Redirect type** — Is the correct redirect (301 vs. 302) chosen based on analytics needs?
- [ ] **Ch 8 — Hash strategy** — Is the hash/encoding approach appropriate (base-62, hash+collision)?
- [ ] **Ch 8 — Collision handling** — Are hash collisions detected and resolved?

---

## 9. Web Crawling (Chapter 9)

### Crawler Design
- [ ] **Ch 9 — URL frontier** — Does the frontier handle politeness and priority?
- [ ] **Ch 9 — Content dedup** — Is content fingerprinting used to avoid redundant crawling?
- [ ] **Ch 9 — URL dedup** — Is a Bloom filter or similar used to track visited URLs?
- [ ] **Ch 9 — Robots.txt** — Is robots.txt respected and cached?
- [ ] **Ch 9 — Spider traps** — Is max URL depth enforced to avoid infinite crawling?

---

## 10. Notifications (Chapter 10)

### Notification System
- [ ] **Ch 10 — Multi-channel** — Are all required channels supported (push, SMS, email)?
- [ ] **Ch 10 — Reliability** — Is a notification log maintained for retry on failure?
- [ ] **Ch 10 — Deduplication** — Are duplicate notifications prevented via event_id checking?
- [ ] **Ch 10 — Rate limiting** — Are per-user notification limits enforced?
- [ ] **Ch 10 — Analytics** — Is notification engagement tracked (open rate, click rate)?
- [ ] **Ch 10 — User preferences** — Can users opt in/out per channel?

---

## 11. News Feed (Chapter 11)

### News Feed System
- [ ] **Ch 11 — Fanout model** — Is the right fanout model chosen (push, pull, or hybrid)?
- [ ] **Ch 11 — Celebrity handling** — Is the celebrity/hotkey problem addressed (hybrid approach)?
- [ ] **Ch 11 — Cache layers** — Are appropriate cache tiers used (feed, content, social graph, actions, counters)?

---

## 12. Chat System (Chapter 12)

### Chat Design
- [ ] **Ch 12 — Protocol** — Is WebSocket used for real-time messaging?
- [ ] **Ch 12 — Stateful servers** — Are chat servers stateful with proper service discovery?
- [ ] **Ch 12 — Storage** — Is a key-value store used for message history (write-heavy)?
- [ ] **Ch 12 — Message sync** — Is per-device cursor-based sync implemented?
- [ ] **Ch 12 — Presence** — Is online presence tracked with heartbeat mechanism?
- [ ] **Ch 12 — Group scaling** — Are small groups (push) and large groups (pull) handled differently?

---

## 13. Autocomplete (Chapter 13)

### Autocomplete System
- [ ] **Ch 13 — Trie structure** — Is a trie used for prefix matching?
- [ ] **Ch 13 — Top-k caching** — Are top-k results cached at each trie node?
- [ ] **Ch 13 — Data pipeline** — Is there a data gathering → aggregation → trie build pipeline?
- [ ] **Ch 13 — Browser caching** — Are autocomplete results cached client-side?
- [ ] **Ch 13 — Content filtering** — Is a filter layer used to remove inappropriate suggestions?
- [ ] **Ch 13 — Sharding** — Is the trie sharded for scale (by character or frequency)?

---

## 14. Video Platform (Chapter 14)

### Video System
- [ ] **Ch 14 — Upload flow** — Is parallel chunked upload with pre-signed URLs used?
- [ ] **Ch 14 — Transcoding** — Is a DAG-based transcoding pipeline designed?
- [ ] **Ch 14 — Adaptive streaming** — Is adaptive bitrate streaming used (HLS/DASH)?
- [ ] **Ch 14 — CDN strategy** — Are popular videos served from CDN, long-tail from origin?
- [ ] **Ch 14 — Error handling** — Are recoverable vs. non-recoverable errors distinguished?
- [ ] **Ch 14 — Content safety** — Is DRM, encryption, or watermarking considered?

---

## 15. Cloud Storage (Chapter 15)

### File Storage System
- [ ] **Ch 15 — Block servers** — Are files split into blocks for delta sync?
- [ ] **Ch 15 — Deduplication** — Are duplicate blocks detected by hash and skipped?
- [ ] **Ch 15 — Resumable uploads** — Are large file uploads resumable?
- [ ] **Ch 15 — Notifications** — Is long polling used for real-time file change notifications?
- [ ] **Ch 15 — Conflict resolution** — Is first-version-wins with conflict copies implemented?
- [ ] **Ch 15 — Versioning** — Is file version history maintained?
- [ ] **Ch 15 — Offline support** — Is an offline backup queue used for sync when clients reconnect?

---

## Quick Review Workflow

1. **Scale pass** — Are scaling fundamentals applied (LB, cache, CDN, replication, sharding)?
2. **Estimation pass** — Are capacity numbers calculated and reasonable?
3. **Structure pass** — Does the design follow the 4-step framework?
4. **Component pass** — Are relevant design patterns used for each component?
5. **Failure pass** — Are failure modes identified and handled?
6. **Trade-off pass** — Are design decisions justified with explicit trade-offs?
7. **Operational pass** — Is monitoring, logging, and alerting included?
8. **Prioritize findings** — Rank by severity: missing scaling > wrong data store > missing estimation > process gaps

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Missing fundamental scaling or wrong architecture | No load balancing, single DB at scale, no caching for read-heavy system, stateful web servers |
| **High** | Missing core design patterns | No capacity estimation, wrong CAP choice, no failure handling, no rate limiting |
| **Medium** | Component design gaps | No CDN, no message queue for async tasks, no content dedup, suboptimal fanout model |
| **Low** | Optimization improvements | No virtual nodes in consistent hashing, no browser caching for autocomplete, no delta sync |
