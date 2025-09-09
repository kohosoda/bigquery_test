{{ config(materialized='view') }}

WITH source_data AS (
    SELECT
        TIMESTAMP(timestamp) AS access_timestamp,
        user_id,
        page_url,
        session_id,
        user_agent,
        ip_address,
        referrer,
        device_type,
        CURRENT_TIMESTAMP() AS loaded_at
    FROM {{ source('ecommerce_data', 'access_logs') }}
)

SELECT * FROM source_data
