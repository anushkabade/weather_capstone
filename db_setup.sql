-- Run this as a superuser or a user with permission to create databases
-- Adjust names as needed
CREATE DATABASE weather_db;

\c weather_db;

-- Table to store raw weather data per city and timestamp
CREATE TABLE IF NOT EXISTS weather_observations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(10),
    observation_time TIMESTAMP NOT NULL,
    temperature_c REAL,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed REAL,
    weather_main VARCHAR(100),
    weather_description TEXT,
    raw_json JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- Index for fast time-range queries
CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_observations (city, observation_time);
