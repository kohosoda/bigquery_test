{{ config(materialized='view') }}

WITH source_data AS (
    SELECT
        order_id,
        user_id,
        order_date,
        total_amount,
        status,
        payment_method,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_data', 'orders') }}
)

SELECT * FROM source_data



