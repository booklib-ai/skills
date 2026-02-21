# After

An event-driven architecture where writes go through a message log, read models are derived via CDC, read replicas serve analytics, and the command/query paths are separated.

```
ARCHITECTURE: E-Commerce Platform (Event-Driven + CQRS)

WRITE PATH
──────────
[Mobile App / Web Browser]
        │ REST (commands only: place order, update product)
        v
[API Gateway]  ──>  [Order Command Service]  ──>  [Orders DB - Postgres]
                                                          │
                                        [Debezium CDC connector]
                                                          │
                                                          v
                                              [Kafka: order.events topic]
                                              (append-only event log,
                                               partitioned by order_id)

READ PATH (derived models — rebuilt from event log, no dual-writes)
──────────────────────────────────────────────────────────────────
[Kafka: order.events]
        │
        ├──> [Inventory Consumer]  ──>  [Inventory Read DB - Postgres replica]
        │                               (product weekly sales view)
        │
        ├──> [Search Consumer]     ──>  [Elasticsearch Index]
        │                               (product search, updated async)
        │
        └──> [Analytics Consumer]  ──>  [BigQuery Streaming Insert]
                                        (append-only fact table,
                                         no load on production DB)

QUERY ENDPOINTS (served from read models, not production write DB)
──────────────────────────────────────────────────────────────────
GET /inventory/reorder-candidates  → Inventory Read DB
GET /search/products?q=...         → Elasticsearch
GET /reports/revenue?period=...    → BigQuery

ASYNC COORDINATION (replaces synchronous call chain)
────────────────────────────────────────────────────
Place order  → write Orders DB → CDC → Kafka
             → Payment Service consumes event → publishes PaymentAuthorized
             → Notification Service consumes PaymentAuthorized → sends email
             (no synchronous chain; each step is independently retried)

CONSISTENCY MODEL
─────────────────
Orders DB       → strongly consistent (single Postgres primary)
Read models     → eventually consistent (seconds of lag, acceptable for reads)
Analytics       → eventually consistent (minutes of lag, acceptable for reports)
```

Key improvements:
- Append-only event log (Kafka) is the single source of truth — derived views are rebuilt from it, never maintained by dual-writes (Ch 11: derived data vs. system of record)
- CDC via Debezium captures changes from the Orders DB atomically — no risk of writing to DB and failing to publish the event (Ch 11: Change Data Capture)
- Analytics consumers write to BigQuery directly from Kafka — no SELECT queries on the production Orders DB (Ch 10: separation of OLTP and OLAP)
- CQRS separates command endpoints (write path) from query endpoints (read path) — each can scale independently
- The synchronous call chain (place order → payment → notification) is replaced by event-driven coordination — failure of one consumer does not block the order write
