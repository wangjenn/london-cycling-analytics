

  create or replace view `custom-range-446703-e1`.`london_cycles`.`stg_journeys`
  OPTIONS()
  as 

SELECT *
FROM `custom-range-446703-e1`.`london_cycles`.`station_popularity`
WHERE station_id IS NOT NULL;

