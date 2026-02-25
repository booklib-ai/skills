# SQL Patterns Reference

Common patterns from *Head First SQL* organized by use case.

## JOIN Patterns

### INNER JOIN — Return only matched rows
```sql
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON c.id = o.customer_id;
```
Use when: You only want rows that have a match in both tables.

### LEFT JOIN — Keep all left rows, NULL for unmatched right
```sql
SELECT c.id, c.name, o.id AS order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;
```
Use when: You want all customers, even those with no orders (order_id will be NULL).

### Anti-join — Find rows with NO match
```sql
SELECT c.id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
```
Use when: You want customers who have NEVER placed an order.

### Many-to-many JOIN through junction table
```sql
SELECT s.name AS student, c.title AS course
FROM students s
INNER JOIN enrollments e ON e.student_id = s.id
INNER JOIN courses c ON c.id = e.course_id;
```
Use when: Two tables have a many-to-many relationship via a junction (bridge) table.

---

## Aggregation Patterns

### Count rows per group
```sql
SELECT department, COUNT(*) AS headcount
FROM employees
GROUP BY department
ORDER BY headcount DESC;
```

### Filter groups with HAVING
```sql
SELECT department, COUNT(*) AS headcount
FROM employees
WHERE active = TRUE          -- filter rows BEFORE grouping
GROUP BY department
HAVING COUNT(*) > 10         -- filter groups AFTER aggregation
ORDER BY headcount DESC;
```

### Aggregate with JOIN
```sql
SELECT
    c.name,
    COUNT(o.id)  AS order_count,
    SUM(o.total) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;
```

---

## NULL Handling Patterns

### Correct NULL comparison
```sql
-- Wrong: = NULL never matches
WHERE phone = NULL

-- Correct
WHERE phone IS NULL
WHERE phone IS NOT NULL
```

### Default value for NULL
```sql
SELECT name, COALESCE(phone, 'N/A') AS phone
FROM customers;
```

### NULL in aggregation
```sql
COUNT(*)         -- counts all rows including NULLs
COUNT(phone)     -- counts only non-NULL phone values
SUM(amount)      -- ignores NULL amounts
AVG(rating)      -- ignores NULL ratings (denominator = non-NULL count)
```

---

## Subquery Patterns

### Derived table (subquery in FROM)
```sql
SELECT dept, avg_salary
FROM (
    SELECT department AS dept, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_averages
WHERE avg_salary > 60000;
```

### CTE (Common Table Expression) — cleaner than nested subquery
```sql
WITH dept_averages AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT department, avg_salary
FROM dept_averages
WHERE avg_salary > 60000;
```

### IN subquery
```sql
SELECT name FROM customers
WHERE id IN (
    SELECT DISTINCT customer_id FROM orders WHERE total > 1000
);
```
Prefer JOIN over IN subquery for large tables — JOINs are generally better optimized.

---

## Transaction Pattern

```sql
BEGIN;

-- Step 1
UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100;

-- Step 2
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Commit only if everything succeeded
COMMIT;

-- On error in application code: ROLLBACK;
```

---

## Index Patterns

### When to add an index
- Columns in WHERE clauses on large tables
- Columns in JOIN ON conditions
- Columns in ORDER BY when LIMIT is used

### Sargable vs non-sargable
```sql
-- Non-sargable: function on column prevents index use
WHERE YEAR(created_at) = 2024
WHERE UPPER(email) = 'TEST@EXAMPLE.COM'

-- Sargable: index can be used
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
WHERE email = 'test@example.com'   -- store emails lowercased
```

---

## Schema Design Patterns

### Foreign key constraint
```sql
CREATE TABLE orders (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    total       DECIMAL(10, 2) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### Junction table for many-to-many
```sql
CREATE TABLE enrollments (
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id)  REFERENCES courses(id)
);
```
