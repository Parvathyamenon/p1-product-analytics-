-- ============================================================
-- P1 - churn_rate.sql
-- QUESTION: What % of last month's active customers did NOT buy this month?
-- TABLE: orders  (columns: customer_id, order_purchase_timestamp, order_status)
-- ============================================================

WITH monthly_customers AS (
    SELECT
        customer_id,
        strftime('%Y-%m', order_purchase_timestamp) AS order_month
    FROM olist_orders_dataset ocd 
    WHERE order_status = 'delivered'
    GROUP BY customer_id, strftime('%Y-%m', order_purchase_timestamp)
),

with_previous AS (
    SELECT
        curr.order_month,
        COUNT(DISTINCT curr.customer_id)                AS current_customers,
        COUNT(DISTINCT prev.customer_id)                AS returning_customers,
        COUNT(DISTINCT curr.customer_id)
            - COUNT(DISTINCT prev.customer_id)          AS churned
    FROM monthly_customers curr
    LEFT JOIN monthly_customers prev
        ON  curr.customer_id = prev.customer_id
        -- SQLite: subtract 1 month using date()
        AND prev.order_month = strftime('%Y-%m', date(curr.order_month || '-01', '-1 month'))
    GROUP BY curr.order_month
)

SELECT
    order_month,
    current_customers,
    returning_customers,
    churned,
    ROUND(100.0 * churned / NULLIF(current_customers, 0), 1) AS churn_rate_pct
FROM with_previous
ORDER BY order_month;
