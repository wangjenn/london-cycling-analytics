{{ config(materialized='table') }}

SELECT
  station_id,
  station_name,
  total_starts,
  total_ends,
  total_traffic,
  net_flow
FROM {{ ref('int_station_popularity') }}
ORDER BY total_traffic DESC
LIMIT 15