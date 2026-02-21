# After

Proper async code using `aiohttp` for non-blocking HTTP, `asyncio.gather` to fetch all three attributes of each product concurrently, and a semaphore to cap simultaneous connections.

```python
import asyncio
import aiohttp

PRODUCT_API   = "https://api.internal.com/products"
INVENTORY_API = "https://api.internal.com/inventory"
PRICING_API   = "https://api.internal.com/pricing"

MAX_CONCURRENT_REQUESTS = 10  # prevent overwhelming the upstream APIs


async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a single JSON endpoint, raising on non-2xx responses."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def build_product_entry(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    product_id: str,
) -> dict:
    """Fetch product, inventory, and pricing concurrently for one product ID."""
    async with semaphore:
        product, inventory, pricing = await asyncio.gather(
            fetch_json(session, f"{PRODUCT_API}/{product_id}"),
            fetch_json(session, f"{INVENTORY_API}/{product_id}"),
            fetch_json(session, f"{PRICING_API}/{product_id}"),
            return_exceptions=False,
        )
    return {
        "id":    product_id,
        "name":  product["name"],
        "stock": inventory["quantity"],
        "price": pricing["amount"],
    }


async def build_product_catalog(product_ids: list[str]) -> list[dict]:
    """Build the full catalog by fetching all products concurrently."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30)
    ) as session:
        tasks = [
            build_product_entry(session, semaphore, pid)
            for pid in product_ids
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    catalog = asyncio.run(build_product_catalog(["sku-001", "sku-002", "sku-003"]))
```

Key improvements:
- `aiohttp.ClientSession` replaces `requests.get` — HTTP calls are non-blocking and never stall the event loop (Ch 4: aiohttp; Ch 2-3: Never block the event loop)
- `asyncio.gather` inside `build_product_entry` fetches product, inventory, and pricing for one SKU concurrently — three sequential blocking calls become one concurrent async fan-out (Ch 3: gather for fan-out)
- The outer `asyncio.gather(*tasks)` processes all product IDs concurrently instead of sequentially in a for loop (Ch 3: create_task / gather)
- `asyncio.Semaphore(10)` limits the number of simultaneous in-flight requests, preventing connection pool exhaustion on the upstream APIs (Ch 3: Semaphore for concurrency control)
- `aiohttp.ClientTimeout(total=30)` ensures no request hangs indefinitely (Ch 3: use timeouts everywhere)
- A single `aiohttp.ClientSession` is reused across all requests for connection pooling — the `async with` context manager ensures it is closed on exit (Ch 4: Use async with for resources)
