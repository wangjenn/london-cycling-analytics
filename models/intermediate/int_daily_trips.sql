{{
    config(
        materialized='view'
    )
}}

SELECT 
  start_date AS date, 
  EXTRACT(DATE FROM start_date) AS trip_date,
  day_of_week,
  COUNT(*) AS total_trips,
  AVG(duration_seconds)/60 AS avg_duration_minutes
FROM {{('london_cycles.trips')}}
GROUP BY
  date, 
  trip_date, 
  day_of_week
ORDER BY
  trip_date
