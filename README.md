# Weather Capstone Project

## Objectives
1. Fetch live weather data from a public API and store it in PostgreSQL.
2. Create required databases and tables in PostgreSQL.
3. Implement visualization of weather data for a single city (analyze last 30 days).
4. Use basic ML models to perform weather forecasting.
5. Produce a PDF report containing objectives, methodology, results and the GitHub repo URL (upload working code to GitHub).

## Structure
- `db_setup.sql` - SQL script to create database and tables.
- `fetch_weather.py` - Fetches data from OpenWeatherMap and inserts into DB.
- `etl_insert.py` - Helper functions for insertion & retrieval.
- `analyze_and_forecast.py` - Visualize last 30 days and run ML models (RandomForest, SARIMAX).
- `create_pdf_template.md` - Markdown template for the PDF report (include your GitHub URL here).
- `requirements.txt` - Python dependencies.
- `.gitignore` - Common ignores.

## How to run (example)
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables (replace placeholders):
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   export PGHOST="localhost"
   export PGPORT="5432"
   export PGUSER="your_pg_user"
   export PGPASSWORD="your_pg_password"
   export PGDATABASE="weather_db"
   ```
3. Create DB and tables:
   ```bash
   psql -U $PGUSER -h $PGHOST -p $PGPORT -f db_setup.sql
   ```
4. Fetch live data (run periodically via cron or systemd timer):
   ```bash
   python fetch_weather.py --city "Mumbai" --interval 3600
   ```
   Or to fetch once:
   ```bash
   python fetch_weather.py --city "Mumbai" --once
   ```
5. Analyze & forecast (this will query last 30 days and save plots + PDF):
   ```bash
   python analyze_and_forecast.py --city "Mumbai" --days 30 --forecast_days 7 --output report_output
   ```

## GitHub upload
- Create a new repository and push this project.
- After pushing, put the repository URL into `create_pdf_template.md` (replace `GITHUB_REPO_URL_HERE`) and then convert to PDF (instructions in the template).

---
Good luck! If you want, I can help you customize any part (DB schema, plots, models) or create a GitHub-ready README with badges.
