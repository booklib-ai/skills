# Before

Python ETL helper with a bare `except`, a mutable default argument bug, and a manual loop that should be a comprehension.

```python
import json
import requests

def fetch_orders(api_url, filters={}):
    # filters dict persists across calls — mutable default arg bug
    filters['status'] = 'completed'
    try:
        response = requests.get(api_url, params=filters)
        data = response.json()
    except:
        # swallows every exception including KeyboardInterrupt
        print("something went wrong")
        return []

    orders = []
    for item in data['orders']:
        if item['total'] > 0:
            order = {
                'id': item['id'],
                'customer': item['customer_name'],
                'total': item['total'],
            }
            orders.append(order)
    return orders


def summarize(orders):
    totals = []
    for o in orders:
        totals.append(o['total'])
    grand_total = 0
    for t in totals:
        grand_total = grand_total + t
    return grand_total
```
