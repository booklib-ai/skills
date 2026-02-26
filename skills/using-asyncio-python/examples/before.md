# Before

An `async def` function that calls the blocking `requests.get()` synchronously, stalling the entire event loop for the duration of each HTTP call.

```python
import asyncio
import requests  # blocking library — not async-safe

PRODUCT_API = "https://api.internal.com/products"
INVENTORY_API = "https://api.internal.com/inventory"
PRICING_API = "https://api.internal.com/pricing"

async def build_product_catalog(product_ids: list[str]) -> list[dict]:
    catalog = []

    for product_id in product_ids:
        # Blocks the event loop for every request — defeats asyncio entirely
        product_resp = requests.get(f"{PRODUCT_API}/{product_id}")
        product = product_resp.json()

        # Called sequentially AND blocking — no concurrency at all
        inv_resp = requests.get(f"{INVENTORY_API}/{product_id}")
        inventory = inv_resp.json()

        price_resp = requests.get(f"{PRICING_API}/{product_id}")
        pricing = price_resp.json()

        catalog.append({
            "id": product_id,
            "name": product["name"],
            "stock": inventory["quantity"],
            "price": pricing["amount"],
        })

    return catalog


asyncio.run(build_product_catalog(["sku-001", "sku-002", "sku-003"]))
```
