{{
    config(
        materialized='view'
    )
}}
SELECT
  station_id,
  station_name,
  COUNT(DISTINCT CASE WHEN type = 'start' THEN rental_id END) AS total_starts,
  COUNT(DISTINCT CASE WHEN type = 'end' THEN rental_id END) AS total_ends,
  COUNT(DISTINCT rental_id) AS total_traffic,
  (COUNT(DISTINCT CASE WHEN type = 'start' THEN rental_id END) - 
   COUNT(DISTINCT CASE WHEN type = 'end' THEN rental_id END)) AS net_flow
FROM (
  -- Union of start and end station data
  SELECT
    rental_id,
    start_station_id AS station_id,
    start_station_name AS station_name,
    'start' AS type
  FROM
    `london_cycles.trips`
  UNION ALL
  SELECT
    rental_id,
    end_station_id AS station_id,
    end_station_name AS station_name,
    'end' AS type
  FROM
    `london_cycles.trips`
) AS station_data
GROUP BY
  station_id, 
  station_name