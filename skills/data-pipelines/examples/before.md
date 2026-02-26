# Before

A Python ETL script that mixes extraction, transformation, and loading in one function with no error handling, no idempotency, and no retry logic.

```python
import psycopg2
import requests
from datetime import datetime

def run_pipeline():
    # Extract: fetch from API
    resp = requests.get("https://api.partner.com/sales/export")
    data = resp.json()

    # Connect to warehouse
    conn = psycopg2.connect("host=dw user=etl dbname=warehouse")
    cur = conn.cursor()

    # Transform + Load: all in one loop, no error handling
    for record in data["sales"]:
        sale_date = datetime.strptime(record["date"], "%Y-%m-%dT%H:%M:%S")
        revenue = float(record["amount_usd"])
        region = record["region"].strip().upper()

        # No upsert — re-running inserts duplicates
        cur.execute("""
            INSERT INTO fact_sales (sale_id, sale_date, revenue, region, loaded_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (record["id"], sale_date, revenue, region))

    conn.commit()
    cur.close()
    conn.close()
    print("done")

run_pipeline()
```
