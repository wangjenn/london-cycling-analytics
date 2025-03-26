{{ config(materialized='table') }}


SELECT
  EXTRACT(year from trip_date) AS year, 
  day_of_week, 
  AVG(total_trips) AS avg_daily_trips
FROM {{ ref('int_daily_trips') }}
GROUP BY EXTRACT(year from trip_date), 
         day_of_week
ORDER BY year, 
         day_of_week