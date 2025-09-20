 Weather Capstone Project

Objectives
1. Fetch live weather data from a public API and store it in PostgreSQL.
2. Create required databases and tables in PostgreSQL.
3. Implement visualization of weather data for a single city (analyze last 30 days).
4. Use basic ML models to perform weather forecasting.
5. Produce a PDF report containing objectives, methodology, results and the GitHub repo URL (upload working code to GitHub).

 Structure
- `db_setup.sql` - SQL script to create database and tables.
- `fetch_weather.py` - Fetches data from OpenWeatherMap and inserts into DB.
- `etl_insert.py` - Helper functions for insertion & retrieval.
- `analyze_and_forecast.py` - Visualize last 30 days and run ML models (RandomForest, SARIMAX).
- `create_pdf_template.md` - Markdown template for the PDF report (include your GitHub URL here).
- `requirements.txt` - Python dependencies.
- `.gitignore` - Common ignores.


