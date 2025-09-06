{{ config(materialized='view') }}

WITH source_data AS (
    SELECT
        product_id,
        name,
        category,
        price,
        created_date,
        brand,
        rating,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_raw', 'products') }}
)

SELECT * FROM source_data



