{{
    config(
        materialized='view'
    )
}}

SELECT *
FROM {{ source('london_cycles', 'trips') }}