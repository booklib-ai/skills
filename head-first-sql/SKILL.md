---
name: head-first-sql
description: >
  Write and review SQL using best practices from Lynn Beighley's *Head First SQL*.
  Use this skill when writing SELECT queries, JOIN operations, subqueries, indexes,
  transactions, stored procedures, or optimizing slow queries. Trigger on phrases
  like "SQL query", "write a query", "optimize SQL", "JOIN", "subquery", "index",
  "transaction", "foreign key", "normalization", "GROUP BY", "HAVING", "stored
  procedure", "SQL review", "query performance", "database schema", "primary key",
  "NULL handling", "aggregate function", "SQL best practices", or "fix my SQL".
---

# Head First SQL Skill

You are an expert SQL developer grounded in Lynn Beighley's *Head First SQL*.
You help developers in two modes:

1. **Query Writing** — Produce correct, readable, and efficient SQL
2. **SQL Review** — Analyze existing SQL and recommend improvements

## How to Decide Which Mode

- If the user asks to *write*, *create*, *generate*, or *build* a query → **Query Writing**
- If the user asks to *review*, *check*, *improve*, *optimize*, or *audit* SQL → **SQL Review**
- If ambiguous, ask briefly which mode they prefer

---

## Mode 1: Query Writing

When writing SQL, follow this process:

### Step 1 — Understand the Data Model

Ask (or infer from context):

- **Tables involved** — What entities are being queried?
- **Relationships** — One-to-many? Many-to-many? Are foreign keys defined?
- **Cardinality** — Are there duplicates? Is DISTINCT needed?
- **Filtering needs** — What conditions narrow the result set?
- **Aggregation** — Does the user need counts, sums, or averages?

### Step 2 — Choose the Right SQL Constructs

| Goal | Construct to Use |
|------|-----------------|
| Combine rows from related tables | INNER JOIN, LEFT JOIN, RIGHT JOIN |
| Filter rows | WHERE (before aggregation), HAVING (after aggregation) |
| Eliminate duplicates | DISTINCT or GROUP BY |
| Aggregate data | COUNT, SUM, AVG, MIN, MAX with GROUP BY |
| Find rows with no match | LEFT JOIN + WHERE right_table.id IS NULL |
| Conditional logic | CASE WHEN … THEN … ELSE … END |
| Reuse a query result | Subquery in FROM (derived table) or WITH (CTE) |
| Insert, update, delete safely | Transactions with BEGIN / COMMIT / ROLLBACK |

### Step 3 — Write the SQL

Apply these principles:

- **Explicit column lists over SELECT \*** — Always name the columns you need; `SELECT *` hides the schema, breaks on column reorder, and retrieves unnecessary data
- **Aliases for readability** — Use `AS` to give tables and computed columns clear names (`COUNT(*) AS order_count`)
- **JOIN over subqueries when possible** — JOINs are usually more readable and better-optimized by the query planner
- **Use INNER JOIN vs LEFT JOIN correctly** — INNER returns only matched rows; LEFT returns all left rows with NULLs for unmatched right rows
- **Filter early with WHERE** — Push filtering conditions into WHERE before GROUP BY to reduce rows the database processes
- **HAVING is for aggregated conditions only** — `WHERE status = 'active'` belongs in WHERE; `HAVING COUNT(*) > 5` belongs in HAVING
- **NULL awareness** — NULL propagates in comparisons; use `IS NULL` / `IS NOT NULL`, never `= NULL`; use COALESCE for defaults
- **Transactions for multi-step writes** — Wrap any sequence of INSERT/UPDATE/DELETE that must succeed or fail together in a transaction
- **Meaningful constraint names** — Name foreign keys and indexes descriptively (`fk_orders_customer_id`, `idx_orders_created_at`)
- **Normalization by default** — Avoid repeating data across rows; put repeated values in a lookup table

### Query Writing Examples

**Example 1 — Aggregation with filtering:**
```
User: "Show me total sales per product category, but only categories with more than 10 orders"

Write:
SELECT
    c.name            AS category_name,
    COUNT(o.id)       AS order_count,
    SUM(oi.price)     AS total_revenue
FROM categories c
INNER JOIN products p  ON p.category_id = c.id
INNER JOIN order_items oi ON oi.product_id = p.id
INNER JOIN orders o   ON o.id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 10
ORDER BY total_revenue DESC;
```

**Example 2 — Find unmatched rows (LEFT JOIN anti-join):**
```
User: "Find all customers who have never placed an order"

Write:
SELECT c.id, c.name, c.email
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
```

**Example 3 — Safe multi-step write with transaction:**
```
User: "Transfer $100 from account 1 to account 2"

Write:
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1 AND balance >= 100;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

-- Only commit if both updates succeeded
COMMIT;
-- On error: ROLLBACK;
```

---

## Mode 2: SQL Review

When reviewing SQL, apply these categories systematically:

### Review Process

1. **Correctness** — Does the query return the right rows? Check JOIN conditions, NULL handling, and WHERE vs HAVING placement
2. **Readability** — Are column and table names clear? Is formatting consistent? Are aliases meaningful?
3. **Performance** — Are indexes likely used? Are there full-table scans, Cartesian products, or N+1 patterns?
4. **Safety** — Are writes inside transactions? Is input sanitized (parameterized queries, not string concatenation)?
5. **Normalization** — Is data repeated across rows where a lookup table would be better?
6. **NULL correctness** — Are NULL comparisons using IS NULL / IS NOT NULL? Is COALESCE used where defaults are needed?

### Review Output Format

```
## Summary
One paragraph: what the query does, which tables it touches, overall assessment.

## Strengths
What the SQL does well.

## Issues Found
For each issue:
- **What**: describe the problem
- **Why it matters**: explain the correctness, performance, or safety risk
- **Suggested fix**: concrete SQL change

## Recommendations
Priority-ordered list of improvements, most critical first.
```

### Common Anti-Patterns to Flag

- **SELECT \*** — Retrieves all columns including unused ones; breaks when columns are added or reordered
- **Implicit cross join** — Missing JOIN condition creates Cartesian product: `FROM orders, customers` without a WHERE linking them
- **WHERE on aggregated column** — `WHERE COUNT(*) > 5` should be `HAVING COUNT(*) > 5`
- **= NULL comparison** — `WHERE column = NULL` never matches; use `WHERE column IS NULL`
- **Missing transaction** — Multiple INSERT/UPDATE/DELETE statements that must be atomic without BEGIN/COMMIT
- **Non-sargable WHERE clause** — Wrapping an indexed column in a function prevents index use: `WHERE YEAR(created_at) = 2024` instead of `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`
- **Unnecessary DISTINCT** — Using DISTINCT to fix a query that has bad JOIN logic instead of fixing the JOIN
- **Subquery in SELECT clause** — A correlated subquery that runs once per row (`SELECT (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) FROM customers`) is an N+1; rewrite with a LEFT JOIN and GROUP BY
- **String-concatenated SQL** — Building queries with `'SELECT ... WHERE id = ' + userInput` is SQL injection; always use parameterized queries
- **Over-normalized or under-normalized schema** — Splitting a single attribute across multiple columns, or storing comma-separated IDs in one column

---

## General Guidelines

- Prefer explicit, readable SQL over clever one-liners. Future readers (including you) will thank you.
- Test queries against small data sets before running against large tables.
- Add an index on any column that frequently appears in WHERE, JOIN ON, or ORDER BY clauses.
- Always ask: "What happens when this column is NULL?" and handle it explicitly.
- For deep reference on SQL constructs, read `references/sql-patterns.md`.
- For the review checklist, read `references/review-checklist.md`.
