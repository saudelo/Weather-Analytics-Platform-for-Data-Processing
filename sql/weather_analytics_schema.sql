--dropping the schema if it exists so i can rerun the script without errors
DROP SCHEMA IF EXISTS weather_analytics CASCADE;

CREATE SCHEMA weather_analytics;

CREATE TABLE weather_analytics.city (
    city_id SERIAL PRIMARY KEY,
    city VARCHAR(50) UNIQUE NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    us_state VARCHAR(50) NULL
    --will clean state using pandas and fill in values if necessary
);

CREATE TABLE weather_analytics.weather_data (
    weather_id SERIAL PRIMARY KEY,
    city_id INT NOT NULL REFERENCES weather_analytics.city (city_id),
    weather_date DATE NOT NULL,
    temp_max_f FLOAT NOT NULL,
    temp_min_f FLOAT NOT NULL,
    temp_mean_f FLOAT NULL,
    precipitation_sum_in FLOAT NOT NULL,
    precipitation_hours FLOAT NULL,
    wind_speed_max_mph FLOAT NOT NULL
--made some fields nullable since some were optional for this assignment
--i will clean any missing values using pandas
);
