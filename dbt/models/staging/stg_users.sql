{{ config(materialized='view') }}

WITH source_data AS (
    SELECT
        user_id,
        name,
        email,
        age,
        gender,
        registration_date,
        city,
        prefecture,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_data', 'users') }}
)

SELECT * FROM source_data



