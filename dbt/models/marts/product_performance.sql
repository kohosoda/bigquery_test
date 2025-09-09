{{ config(materialized='table') }}

WITH product_sales AS (
    SELECT
        p.product_id,
        p.name AS product_name,
        p.category,
        p.price,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COALESCE(SUM(oi.quantity), 0) AS total_quantity_sold,
        COALESCE(SUM(oi.line_total), 0) AS total_revenue
    FROM {{ ref('stg_products') }} p
    LEFT JOIN {{ ref('stg_order_items') }} oi ON p.product_id = oi.product_id
    LEFT JOIN {{ ref('stg_orders') }} o ON oi.order_id = o.order_id AND o.status = '完了'
    GROUP BY 1, 2, 3, 4
)

SELECT
    *,
    CASE 
        WHEN total_quantity_sold > 0 THEN 
            ROUND(total_revenue / total_quantity_sold, 2)
        ELSE 0
    END AS avg_unit_price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_revenue DESC) 
        AS revenue_rank_in_category,
    CURRENT_TIMESTAMP() AS processed_at
FROM product_sales
