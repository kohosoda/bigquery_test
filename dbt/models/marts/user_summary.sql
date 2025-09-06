{{ config(materialized='table') }}

WITH user_orders AS (
    SELECT
        u.user_id,
        u.name,
        u.email,
        u.age,
        u.gender,
        u.city,
        u.prefecture,
        u.registration_date,
        COUNT(o.order_id) AS total_orders,
        COALESCE(SUM(o.total_amount), 0) AS total_amount,
        COALESCE(AVG(o.total_amount), 0) AS avg_order_value
    FROM {{ ref('stg_users') }} u
    LEFT JOIN {{ ref('stg_orders') }} o 
        ON u.user_id = o.user_id 
        AND o.status = '完了'
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8
)

SELECT
    *,
    CASE
        WHEN total_orders = 0 THEN '未購入'
        WHEN total_orders = 1 THEN '新規顧客'
        WHEN total_orders BETWEEN 2 AND 5 THEN 'リピーター'
        WHEN total_orders > 5 THEN 'ロイヤル顧客'
    END AS customer_segment,
    CURRENT_TIMESTAMP() AS processed_at
FROM user_orders
