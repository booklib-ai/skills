# Before

A SQL query with multiple issues: SELECT *, missing transaction, correlated subquery N+1, and incorrect NULL comparison.

```sql
-- Get all customers, their total orders, and flag customers with no phone
SELECT *
FROM customers, orders
WHERE customers.id = orders.customer_id
AND orders.status != NULL
AND (
    SELECT COUNT(*)
    FROM order_items
    WHERE order_items.order_id = orders.id
) > 0;
```

Problems in this query:
1. `SELECT *` — returns every column from both tables (including duplicates like `id`)
2. Implicit cross join syntax (`FROM customers, orders`) — harder to read than explicit JOIN
3. `!= NULL` — never matches any row; NULL comparisons require `IS NOT NULL`
4. Correlated subquery in WHERE runs once per row — N+1 performance problem
5. No transaction wrapping when this is used alongside writes
