# After

Pythonic code with specific exception handling, a dataclass for structure, a comprehension for filtering, and no mutable default argument.

```python
import requests
from dataclasses import dataclass
from requests.exceptions import HTTPError, ConnectionError, Timeout

@dataclass
class Order:
    id: str
    customer: str
    total: float


def fetch_orders(api_url: str, filters: dict | None = None) -> list[Order]:
    """Fetch completed orders from the partner API.

    Args:
        api_url: Base URL for the orders endpoint.
        filters: Optional extra query parameters. Defaults to empty dict.

    Returns:
        List of Order dataclasses for all completed orders with positive totals.

    Raises:
        HTTPError: If the API returns a non-2xx response.
        ConnectionError: If the API is unreachable.
        Timeout: If the request exceeds the timeout threshold.
    """
    params = {"status": "completed", **(filters or {})}

    response = requests.get(api_url, params=params, timeout=10)
    response.raise_for_status()  # raises HTTPError for 4xx/5xx

    data = response.json()
    return [
        Order(id=item["id"], customer=item["customer_name"], total=item["total"])
        for item in data["orders"]
        if item["total"] > 0
    ]


def summarize(orders: list[Order]) -> float:
    """Return the grand total revenue across all orders."""
    return sum(order.total for order in orders)
```

Key improvements:
- `filters: dict | None = None` with `filters or {}` fixes the mutable default argument bug (Item 24: Use None as a default for mutable default arguments)
- Specific exceptions `HTTPError`, `ConnectionError`, `Timeout` replace the bare `except` clause — errors propagate appropriately and `KeyboardInterrupt` is no longer swallowed (Item 65: Handle exceptions specifically)
- `response.raise_for_status()` replaces silent failure on bad HTTP responses
- List comprehension with inline `if` replaces the manual `append` loop (Item 27: Use Comprehensions Instead of map and filter)
- `@dataclass` replaces a raw `dict` for the order structure — typed, readable, and self-documenting (Item 37: Compose Classes Instead of Nesting Many Levels of Built-in Types)
- `sum(order.total for order in orders)` in `summarize` is a single idiomatic expression, no intermediate list needed
