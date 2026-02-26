# After

A clean pipeline with separated extract/transform/load functions, idempotent upserts, retry logic, and proper error handling.

```python
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

import psycopg2
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


@dataclass
class SaleRecord:
    id: str
    sale_date: datetime
    revenue: float
    region: str


def with_retry(max_attempts: int = 3, backoff_seconds: float = 2.0):
    """Decorator: retry a function on transient failures with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except (RequestException, psycopg2.OperationalError) as exc:
                    if attempt == max_attempts:
                        raise
                    wait = backoff_seconds ** attempt
                    logger.warning("Attempt %d/%d failed: %s — retrying in %.1fs",
                                   attempt, max_attempts, exc, wait)
                    time.sleep(wait)
        return wrapper
    return decorator


@with_retry(max_attempts=3)
def extract(api_url: str) -> list[dict]:
    """Fetch raw sales records from the partner API."""
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    return response.json()["sales"]


def transform(raw_records: list[dict]) -> list[SaleRecord]:
    """Parse and normalise raw API records into typed SaleRecord objects."""
    return [
        SaleRecord(
            id=rec["id"],
            sale_date=datetime.fromisoformat(rec["date"]),
            revenue=float(rec["amount_usd"]),
            region=rec["region"].strip().upper(),
        )
        for rec in raw_records
    ]


def load(records: list[SaleRecord], dsn: str) -> int:
    """Upsert records into fact_sales. Idempotent: re-running is safe."""
    upsert_sql = """
        INSERT INTO fact_sales (sale_id, sale_date, revenue, region, loaded_at)
        VALUES (%(id)s, %(sale_date)s, %(revenue)s, %(region)s, NOW())
        ON CONFLICT (sale_id) DO UPDATE
            SET revenue   = EXCLUDED.revenue,
                loaded_at = EXCLUDED.loaded_at
    """
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        cur.executemany(upsert_sql, [vars(r) for r in records])
        loaded = cur.rowcount
    logger.info("Upserted %d records into fact_sales", loaded)
    return loaded


def run_pipeline(api_url: str, warehouse_dsn: str) -> None:
    logger.info("Starting sales pipeline")
    raw = extract(api_url)
    records = transform(raw)
    loaded = load(records, warehouse_dsn)
    logger.info("Pipeline complete: %d records loaded", loaded)
```

Key improvements:
- Extract, transform, and load are separate functions with single responsibilities — each is independently testable and replaceable (Ch 13: Best Practices — separation of concerns)
- `ON CONFLICT (sale_id) DO UPDATE` makes the load idempotent — re-running the pipeline never creates duplicate rows (Ch 13: Idempotency)
- `@with_retry` decorator handles transient API and database failures with exponential backoff (Ch 6: API Ingestion — retry logic)
- `SaleRecord` dataclass replaces a raw dict, providing type safety and named field access in the transform step
- `psycopg2.connect` used as a context manager ensures the connection and transaction are always closed and committed correctly (Ch 4: Database Ingestion)
- Structured logging with `logger.info/warning` replaces bare `print` — output is filterable and includes context (Ch 12: Monitoring)
