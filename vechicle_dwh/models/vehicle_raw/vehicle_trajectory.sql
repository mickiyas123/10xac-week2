{{ config(
    materialized='table',
) }}

with raw_vehicle_trajectory as (
    select
        id,
        lat,
        lon,
        speed,
        lon_acc,
        lat_acc,
        time,
        track_id
        from {{ source('week_two', 'raw_vehicle_trajectory') }}
)

select
    id::int,
    lat::float,
    lon::float,
    speed::float,
    lon_acc::float,
    lat_acc::float,
    time::float,
    v.track_id
from raw_vehicle_trajectory vt 
left join {{ ref('vehicle') }} v
on v.track_id = vt.track_id