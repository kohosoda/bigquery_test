{{ config(materialized='table') }}

WITH daily_metrics AS (
    SELECT
        DATE(o.order_date) AS order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.user_id) AS unique_customers,
        COALESCE(SUM(o.total_amount), 0) AS total_revenue,
        COALESCE(AVG(o.total_amount), 0) AS avg_order_value
    FROM {{ ref('stg_orders') }} o
    WHERE o.status = '完了'
    GROUP BY 1
)

SELECT
    *,
    -- 7日間移動平均
    AVG(total_revenue) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_7day_avg,
    -- 前日比
    LAG(total_revenue) OVER (ORDER BY order_date) AS prev_day_revenue,
    CURRENT_TIMESTAMP() AS processed_at
FROM daily_metrics
ORDER BY order_date
