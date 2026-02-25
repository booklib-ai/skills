# After

The same query rewritten with explicit JOINs, correct NULL handling, named columns, and the N+1 correlated subquery eliminated.

```sql
-- Get customers with at least one order, showing their order count and total spend
SELECT
    c.id              AS customer_id,
    c.name            AS customer_name,
    c.email,
    COUNT(o.id)       AS order_count,
    SUM(oi.price)     AS total_spend
FROM customers c
INNER JOIN orders o
    ON o.customer_id = c.id
   AND o.status IS NOT NULL        -- correct NULL check
INNER JOIN order_items oi
    ON oi.order_id = o.id
GROUP BY c.id, c.name, c.email
HAVING COUNT(o.id) > 0            -- filter after aggregation
ORDER BY total_spend DESC;
```

Key improvements:
- **Explicit column list** replaces `SELECT *` — callers see exactly what they get; adding a column to the table won't silently break this query
- **INNER JOIN … ON** replaces implicit cross join — the relationship between tables is visible in the query structure
- **`IS NOT NULL`** replaces `!= NULL` — NULL comparisons with `=` or `!=` always return unknown (not TRUE), so they silently drop rows; `IS NOT NULL` is correct
- **JOIN + GROUP BY** replaces the correlated subquery — the database executes one scan instead of one subquery per row; performance scales linearly rather than quadratically
- **HAVING COUNT(o.id) > 0** filters after aggregation — only customers with matched orders appear; this is equivalent logic to the original intent, done correctly
- **Column aliases** (`customer_id`, `order_count`, `total_spend`) make the result set self-documenting for application code consuming it
