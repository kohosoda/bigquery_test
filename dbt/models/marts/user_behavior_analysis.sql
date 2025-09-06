{{ config(materialized='table') }}

WITH user_web_activity AS (
    SELECT
        user_id,
        COUNT(*) AS total_page_views,
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(DISTINCT DATE(access_timestamp)) AS active_days,
        COUNT(CASE WHEN page_url LIKE '%/product/%' THEN 1 END) AS product_page_views,
        COUNT(CASE WHEN page_url = '/cart' THEN 1 END) AS cart_views,
        COUNT(CASE WHEN page_url = '/checkout' THEN 1 END) AS checkout_views
    FROM {{ ref('stg_access_logs') }}
    WHERE user_id IS NOT NULL
    GROUP BY 1
),

user_purchase_activity AS (
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS total_orders,
        COALESCE(SUM(total_amount), 0) AS total_spent
    FROM {{ ref('stg_orders') }}
    WHERE status = '完了'
    GROUP BY 1
)

SELECT
    COALESCE(w.user_id, p.user_id) AS user_id,
    COALESCE(w.total_page_views, 0) AS total_page_views,
    COALESCE(w.total_sessions, 0) AS total_sessions,
    COALESCE(w.active_days, 0) AS active_days,
    COALESCE(w.product_page_views, 0) AS product_page_views,
    COALESCE(w.cart_views, 0) AS cart_views,
    COALESCE(w.checkout_views, 0) AS checkout_views,
    COALESCE(p.total_orders, 0) AS total_orders,
    COALESCE(p.total_spent, 0) AS total_spent,
    
    -- コンバージョン率の計算
    CASE 
        WHEN w.total_sessions > 0 THEN 
            ROUND(COALESCE(p.total_orders, 0) / w.total_sessions * 100, 2)
        ELSE 0
    END AS session_conversion_rate,
    
    -- カート離脱率
    CASE 
        WHEN w.cart_views > 0 THEN 
            ROUND((w.cart_views - COALESCE(w.checkout_views, 0)) / w.cart_views * 100, 2)
        ELSE 0
    END AS cart_abandonment_rate,
    
    CURRENT_TIMESTAMP() AS processed_at
FROM user_web_activity w
FULL OUTER JOIN user_purchase_activity p ON w.user_id = p.user_id
