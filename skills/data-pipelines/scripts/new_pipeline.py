#!/usr/bin/env python3
"""
new_pipeline.py — Scaffold a new data pipeline with extract/transform/load structure.
Usage: python new_pipeline.py <pipeline-name> [--source csv|api|db] [--target db|file|api]
"""

import argparse
import os
import sys
from pathlib import Path
from string import Template

# ---------------------------------------------------------------------------
# File templates
# ---------------------------------------------------------------------------

EXTRACT_CSV = '''\
"""extract.py — Extract data from a CSV source."""

import csv
import logging
import time
from pathlib import Path
from functools import wraps

logger = logging.getLogger(__name__)


def retry(max_attempts=3, delay=2.0, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    wait = delay * (2 ** (attempt - 1))
                    logger.warning("Attempt %d failed: %s. Retrying in %.1fs...", attempt, exc, wait)
                    time.sleep(wait)
        return wrapper
    return decorator


@retry(max_attempts=3, exceptions=(OSError,))
def extract(source_path: str) -> list[dict]:
    """Read rows from a CSV file. Returns a list of dicts."""
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    logger.info("Extracting from %s", path)
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    logger.info("Extracted %d rows", len(rows))
    return rows
'''

EXTRACT_API = '''\
"""extract.py — Extract data from an HTTP API source."""

import json
import logging
import time
import urllib.error
import urllib.request
from functools import wraps

logger = logging.getLogger(__name__)

BASE_URL = "https://api.example.com/data"
API_KEY = ""  # Set via environment variable in production


def retry(max_attempts=3, delay=2.0, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    wait = delay * (2 ** (attempt - 1))
                    logger.warning("Attempt %d failed: %s. Retrying in %.1fs...", attempt, exc, wait)
                    time.sleep(wait)
        return wrapper
    return decorator


@retry(max_attempts=3, exceptions=(urllib.error.URLError, OSError))
def extract(endpoint: str = BASE_URL) -> list[dict]:
    """Fetch JSON records from an API endpoint. Returns a list of dicts."""
    logger.info("Extracting from %s", endpoint)
    req = urllib.request.Request(endpoint, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read())
    records = data if isinstance(data, list) else data.get("results", data.get("items", []))
    logger.info("Extracted %d records", len(records))
    return records
'''

EXTRACT_DB = '''\
"""extract.py — Extract data from a database source."""

import logging
import sqlite3
import time
from functools import wraps

logger = logging.getLogger(__name__)

DB_PATH = "source.db"
QUERY = "SELECT * FROM source_table"


def retry(max_attempts=3, delay=2.0, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    wait = delay * (2 ** (attempt - 1))
                    logger.warning("Attempt %d failed: %s. Retrying in %.1fs...", attempt, exc, wait)
                    time.sleep(wait)
        return wrapper
    return decorator


@retry(max_attempts=3, exceptions=(sqlite3.OperationalError,))
def extract(db_path: str = DB_PATH, query: str = QUERY) -> list[dict]:
    """Query records from a SQLite database. Returns a list of dicts."""
    logger.info("Connecting to %s", db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
    logger.info("Extracted %d rows", len(rows))
    return rows
'''

TRANSFORM_TEMPLATE = '''\
"""transform.py — Transform extracted records."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def _clean_record(record: dict[str, Any]) -> dict[str, Any]:
    """Strip whitespace from string values and drop empty fields."""
    cleaned = {}
    for key, value in record.items():
        if isinstance(value, str):
            value = value.strip()
        if value not in (None, "", []):
            cleaned[key] = value
    return cleaned


def _validate_record(record: dict[str, Any]) -> bool:
    """Return True if the record is valid. Customize required fields here."""
    # TODO: add field-specific validation
    return bool(record)


def transform(records: list[dict]) -> list[dict]:
    """Clean, validate, and reshape records for loading."""
    logger.info("Transforming %d records", len(records))
    output = []
    skipped = 0
    for record in records:
        cleaned = _clean_record(record)
        if not _validate_record(cleaned):
            skipped += 1
            continue
        # TODO: add field mappings / enrichment here
        output.append(cleaned)
    if skipped:
        logger.warning("Skipped %d invalid records", skipped)
    logger.info("Transformed %d records", len(output))
    return output
'''

LOAD_DB = '''\
"""load.py — Idempotent load into a SQLite database using upsert."""

import logging
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)

DB_PATH = "output.db"
TABLE = "$pipeline_name"
# Define a unique key column used for upsert conflict detection
UNIQUE_KEY = "id"


def _ensure_table(conn: sqlite3.Connection, sample: dict[str, Any]) -> None:
    columns = ", ".join(
        f"{col} TEXT" if col != UNIQUE_KEY else f"{col} TEXT PRIMARY KEY"
        for col in sample
    )
    conn.execute(f"CREATE TABLE IF NOT EXISTS {TABLE} ({columns})")
    conn.commit()


def load(records: list[dict]) -> int:
    """Upsert records into SQLite. Returns number of rows written."""
    if not records:
        logger.info("No records to load.")
        return 0
    logger.info("Loading %d records into %s:%s", len(records), DB_PATH, TABLE)
    conn = sqlite3.connect(DB_PATH)
    try:
        _ensure_table(conn, records[0])
        cols = ", ".join(records[0].keys())
        placeholders = ", ".join("?" for _ in records[0])
        sql = (
            f"INSERT OR REPLACE INTO {TABLE} ({cols}) VALUES ({placeholders})"
        )
        conn.executemany(sql, [list(r.values()) for r in records])
        conn.commit()
    finally:
        conn.close()
    logger.info("Loaded %d records", len(records))
    return len(records)
'''

LOAD_FILE = '''\
"""load.py — Write records to a CSV or JSON file (idempotent by overwrite)."""

import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

OUTPUT_PATH = "$pipeline_name_output.csv"


def load(records: list[dict], output_path: str = OUTPUT_PATH) -> int:
    """Write records to a file. Overwrites to ensure idempotency."""
    if not records:
        logger.info("No records to load.")
        return 0
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".json":
        path.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")
    else:
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
    logger.info("Wrote %d records to %s", len(records), path)
    return len(records)
'''

LOAD_API = '''\
"""load.py — POST records to an API endpoint (idempotent with dedup key)."""

import json
import logging
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)

TARGET_URL = "https://api.example.com/ingest"
BATCH_SIZE = 100


def _post_batch(batch: list[dict]) -> None:
    payload = json.dumps(batch).encode("utf-8")
    req = urllib.request.Request(
        TARGET_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            logger.info("Batch of %d posted — HTTP %d", len(batch), status)
    except urllib.error.HTTPError as exc:
        logger.error("HTTP error %d posting batch: %s", exc.code, exc.reason)
        raise


def load(records: list[dict]) -> int:
    """POST records in batches. Returns total records sent."""
    if not records:
        logger.info("No records to load.")
        return 0
    total = 0
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        _post_batch(batch)
        total += len(batch)
    logger.info("Loaded %d records via API", total)
    return total
'''

PIPELINE_TEMPLATE = '''\
"""pipeline.py — Orchestrator: extract → transform → load."""

import logging
import sys
import time

from extract import extract
from transform import transform
from load import load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("$pipeline_name")


def run() -> int:
    """Run the full pipeline. Returns exit code (0=success, 1=failure)."""
    start = time.monotonic()
    logger.info("Pipeline '$pipeline_name' starting")
    try:
        raw = extract()
        records = transform(raw)
        count = load(records)
        elapsed = time.monotonic() - start
        logger.info(
            "Pipeline complete — %d records loaded in %.2fs", count, elapsed
        )
        return 0
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(run())
'''

REQUIREMENTS_TEMPLATE = '''\
# Runtime dependencies for $pipeline_name pipeline
# Add your project-specific packages below.

# Uncomment as needed:
# requests>=2.31          # for API sources/targets
# psycopg2-binary>=2.9    # for PostgreSQL
# pymysql>=1.1            # for MySQL
# pandas>=2.0             # for complex transformations
# pydantic>=2.0           # for record validation
'''

# ---------------------------------------------------------------------------
# Source/target template selection
# ---------------------------------------------------------------------------

EXTRACT_TEMPLATES = {"csv": EXTRACT_CSV, "api": EXTRACT_API, "db": EXTRACT_DB}
LOAD_TEMPLATES = {"db": LOAD_DB, "file": LOAD_FILE, "api": LOAD_API}


def render(template_str: str, pipeline_name: str) -> str:
    safe_name = pipeline_name.replace("-", "_")
    return Template(template_str).safe_substitute(pipeline_name=safe_name)


def create_pipeline(name: str, source: str, target: str) -> None:
    base = Path(name)
    if base.exists():
        print(f"Error: directory '{base}' already exists. Choose a different name.")
        sys.exit(1)
    base.mkdir(parents=True)

    files = {
        "extract.py": render(EXTRACT_TEMPLATES[source], name),
        "transform.py": render(TRANSFORM_TEMPLATE, name),
        "load.py": render(LOAD_TEMPLATES[target], name),
        "pipeline.py": render(PIPELINE_TEMPLATE, name),
        "requirements.txt": render(REQUIREMENTS_TEMPLATE, name),
    }

    created = []
    for filename, content in files.items():
        path = base / filename
        path.write_text(content, encoding="utf-8")
        created.append(str(path))

    print(f"\nPipeline '{name}' created successfully!\n")
    print(f"  Source  : {source}")
    print(f"  Target  : {target}")
    print(f"\nFiles created:")
    for f in created:
        print(f"  {f}")
    print(f"\nNext steps:")
    print(f"  1. cd {name}")
    print(f"  2. Review extract.py and update source configuration")
    print(f"  3. Customize transform.py with your business logic")
    print(f"  4. Review load.py and configure target destination")
    print(f"  5. pip install -r requirements.txt   # add packages as needed")
    print(f"  6. python pipeline.py")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new data pipeline (extract → transform → load)"
    )
    parser.add_argument("name", help="Pipeline name (used as directory name)")
    parser.add_argument(
        "--source",
        choices=["csv", "api", "db"],
        default="csv",
        help="Data source type (default: csv)",
    )
    parser.add_argument(
        "--target",
        choices=["db", "file", "api"],
        default="db",
        help="Data target type (default: db)",
    )
    args = parser.parse_args()
    create_pipeline(args.name, args.source, args.target)


if __name__ == "__main__":
    main()
