{{ 
    config(
        materialized='table',
        primary_key='track_id'
        )
    }}

with raw_vehicle as (
    select
        track_id,
        type,
        traveled_d,
        avg_speed
        from {{  source('week_two', 'raw_vehicle') }}
)

select
    track_id::int,
    type::text,
    traveled_d::float,
    avg_speed::float
from raw_vehicle
