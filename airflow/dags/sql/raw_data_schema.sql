create table if not exists raw_vehicle (
    track_id SERIAL PRIMARY KEY,
    type VARCHAR(255),
    traveled_d FLOAT,
    avg_speed FLOAT
);
create table if not exists raw_vehicle_trajectory(
    id SERIAL PRIMARY KEY,
    lat FLOAT,
    lon FLOAT,
    speed FLOAT,
    lon_acc FLOAT,
    lat_acc FLOAT,
    time FLOAT,
    track_id INTEGER REFERENCES raw_vehicle(track_id)
);

-- create type if not exists status_enum AS ENUM ('completed', 'failed');

create table if not exists csv_file_name(
    id  SERIAL PRIMARY KEY,
    name VARCHAR(500),
    status VARCHAR(100)
)