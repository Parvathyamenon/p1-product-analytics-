
-- P1 - cohort_retention.sql
-- QUESTION: What % of customers from each monthly cohort return to buy again?
-- TABLE: orders  (columns: customer_id, order_purchase_timestamp, order_status)
-- ============================================================

-- STEP 1: Find each customer's first purchase month (their 'cohort month')
WITH cohort_base AS (
    SELECT
        customer_id,
        strftime('%Y-%m', MIN(order_purchase_timestamp)) AS cohort_month
    FROM olist_orders_dataset ood 
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

-- STEP 2: For each order, find how many months after cohort it happened
order_cohorts AS (
    SELECT
        o.customer_id,
        c.cohort_month,
        strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
        -- SQLite: calculate month difference using year*12 + month arithmetic
        (
            (CAST(strftime('%Y', o.order_purchase_timestamp) AS INTEGER) * 12
             + CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER))
            -
            (CAST(substr(c.cohort_month, 1, 4) AS INTEGER) * 12
             + CAST(substr(c.cohort_month, 6, 2) AS INTEGER))
        ) AS month_number
    FROM olist_orders_dataset o
    JOIN cohort_base c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
),

-- STEP 3: Count cohort size
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM cohort_base
    GROUP BY cohort_month
),

retention_counts AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM order_cohorts
    GROUP BY cohort_month, month_number
)

-- FINAL: Retention rate = active / cohort_size * 100
SELECT
    r.cohort_month,
    r.month_number,
    r.active_customers,
    s.cohort_customers,
    ROUND(100.0 * r.active_customers / s.cohort_customers, 1) AS retention_rate_pct
FROM retention_counts r
JOIN cohort_size s ON r.cohort_month = s.cohort_month
ORDER BY r.cohort_month, r.month_number;
