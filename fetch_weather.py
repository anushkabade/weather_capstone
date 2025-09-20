
#!/usr/bin/env python3
"""Fetch weather from OpenWeatherMap and store in PostgreSQL.

Usage examples:
  export OPENWEATHER_API_KEY=...
  export PGHOST=localhost PGPORT=5432 PGUSER=pguser PGPASSWORD=pgpass PGDATABASE=weather_db
  python fetch_weather.py --city "Mumbai" --once
  python fetch_weather.py --city "Mumbai" --interval 3600  # run forever every hour
"""
import os, time, argparse, requests, psycopg2, json
from datetime import datetime, timezone

API = os.getenv('OPENWEATHER_API_KEY')
if not API:
    raise SystemExit('Please set OPENWEATHER_API_KEY environment variable.')

DB_PARAMS = {
    'host': os.getenv('PGHOST','localhost'),
    'port': int(os.getenv('PGPORT',5432)),
    'user': os.getenv('PGUSER','postgres'),
    'password': os.getenv('PGPASSWORD',''),
    'dbname': os.getenv('PGDATABASE','weather_db'),
}

def fetch_city_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric'
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def insert_into_db(payload):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    obs_time = datetime.utcfromtimestamp(payload.get('dt')).replace(tzinfo=timezone.utc)
    cur.execute("""INSERT INTO weather_observations
        (city,country,observation_time,temperature_c,humidity,pressure,wind_speed,weather_main,weather_description,raw_json)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        payload.get('name'),
        payload.get('sys',{}).get('country'),
        obs_time,
        payload.get('main',{}).get('temp'),
        payload.get('main',{}).get('humidity'),
        payload.get('main',{}).get('pressure'),
        payload.get('wind',{}).get('speed'),
        payload.get('weather',[{}])[0].get('main'),
        payload.get('weather',[{}])[0].get('description'),
        json.dumps(payload)
    ))
    conn.commit()
    cur.close()
    conn.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', required=True, help='City name, e.g. "Mumbai"')
    parser.add_argument('--interval', type=int, help='Polling interval in seconds. If not given, run once.')
    parser.add_argument('--once', action='store_true', help='Run once and exit.')
    args = parser.parse_args()

    if args.interval and args.once:
        parser.error('Use either --interval or --once, not both.')
    if not args.interval and not args.once:
        # default run once
        args.once = True

    try:
        while True:
            payload = fetch_city_weather(args.city)
            insert_into_db(payload)
            print(f"Inserted observation for {args.city} at {payload.get('dt')}")
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print('Stopped by user')

if __name__ == '__main__':
    main()
