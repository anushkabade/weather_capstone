# Weather Capstone Report

**Project Title:** Weather Forecasting Capstone

**Author:** Your Name

**GitHub Repository:** GITHUB_REPO_URL_HERE

## Objectives
- Fetch live weather data from a public API and store it in PostgreSQL.
- Create databases and tables in PostgreSQL.
- Visualize weather data for a single city (last 30 days).
- Use basic ML prediction models to do weather forecasting.

## Methodology
1. Data collection: OpenWeatherMap API (or similar). Store raw JSON and parsed fields in PostgreSQL.
2. Database design: `weather_observations` table (see db_setup.sql).
3. Analysis: Query last 30 days and resample hourly, plot temperature/humidity.
4. Forecasting: RandomForest with lag features and SARIMAX for time-series.

## Results
(Include plots, metrics, and discussion here.)

## GitHub URL
GITHUB_REPO_URL_HERE

## How to reproduce
(Provide environment, commands, and any notes.)
