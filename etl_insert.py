import os, psycopg2, pandas as pd, requests, json  # ← added json

# DB parameters
DB_PARAMS = {
    'host': os.getenv('PGHOST', 'localhost'),
    'port': int(os.getenv('PGPORT', 5432)),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', ''),
    'dbname': os.getenv('PGDATABASE', 'weather_db'),
}

city = "Mumbai"

# Get API key from environment
api_key = os.environ.get("OPENWEATHER_API_KEY")
if not api_key:
    raise ValueError("Please set OPENWEATHER_API_KEY environment variable")

# Call OpenWeatherMap API
api_url = "http://api.openweathermap.org/data/2.5/weather"
params = {"q": city, "appid": api_key, "units": "metric"}

print(f"Fetching weather for city: {city}")
response = requests.get(api_url, params=params)
print(f"API response status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Fetched temperature: {data['main']['temp']} °C")

    # Insert data into PostgreSQL
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_observations (
            city, country, observation_time, temperature_c, humidity,
            pressure, wind_speed, weather_main, weather_description, raw_json
        ) VALUES (%s,%s,now(),%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['name'],
        data['sys']['country'],
        data['main']['temp'],
        data['main']['humidity'],
        data['main']['pressure'],
        data['wind']['speed'],
        data['weather'][0]['main'],
        data['weather'][0]['description'],
        json.dumps(data)   # ✅ Proper JSON conversion
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Data inserted for {city}")
else:
    print(f"Failed to fetch data: {response.text}")

