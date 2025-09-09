{{ config(materialized='view') }}

WITH source_data AS (
    SELECT
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        quantity * unit_price AS line_total,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_data', 'order_items') }}
)

SELECT * FROM source_data



