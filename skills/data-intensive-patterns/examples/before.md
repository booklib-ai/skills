# Before

A text architecture diagram showing an e-commerce platform where every component communicates synchronously via REST with no event log, no read replicas, and no separation of read/write paths.

```
ARCHITECTURE: E-Commerce Platform (Synchronous REST Only)

[Mobile App] ──REST──> [API Server]
[Web Browser] ──REST──> [API Server]
                              │
              ┌───────────────┼──────────────────┐
              │               │                  │
              v               v                  v
        [Order DB]     [Product DB]       [User DB]
         (Postgres)     (Postgres)        (Postgres)
              │               │
              v               v
     [Analytics REST]  [Search REST]    (both query
      calls Order DB    calls Product    production
      directly via      DB directly      DBs live)
      SQL over HTTP

FLOWS:
  Place order   → API → write Order DB → REST call to
                  Inventory Service → REST call to
                  Payment Service → REST call to
                  Notification Service
                  (all synchronous, chain fails if any step fails)

  Dashboard     → API → query Order DB, Product DB, User DB
                  in sequence (3 serial DB queries on write path)

  Search        → API → query Product DB directly
                  (full table scans, no index service)

  Reports       → Analytics service polls Order DB every 5 min
                  via REST (puts load on production DB)
```
