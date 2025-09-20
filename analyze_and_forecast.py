
#!/usr/bin/env python3
"""Analyze last N days for a city and produce visualizations and forecasts.

Produces:
 - temperature_plot_{city}.png
 - humidity_plot_{city}.png
 - forecast_plot_{city}.png
 - simple PDF report named report_{city}.pdf
"""
import argparse, os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
from etl_insert import get_last_n_days
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def plot_series(df, city, column, out_prefix):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df.index, df[column], marker='o', linewidth=1)
    ax.set_title(f"{column} for {city} (last {len(df)} points)")
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel(column)
    fig.autofmt_xdate(rotation=45)
    out = f"{out_prefix}_{column.lower()}_{city.replace(' ','_')}.png"
    fig.savefig(out, bbox_inches='tight')
    plt.close(fig)
    return out

def rf_forecast(df, steps=7, column='temperature_c'):
    # create lag features
    df = df.copy()
    for lag in range(1,25):
        df[f'lag_{lag}'] = df[column].shift(lag)
    df = df.dropna()
    X = df[[c for c in df.columns if c.startswith('lag_')]]
    y = df[column]
    # train/test split: last 20% as test
    split = int(len(X)*0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    # iterative forecast
    last_row = X.iloc[-1].values.reshape(1,-1)
    preds = []
    cur_features = last_row.flatten()
    for _ in range(steps):
        pred = model.predict(cur_features.reshape(1,-1))[0]
        preds.append(pred)
        # shift features
        cur_features = np.roll(cur_features, 1)
        cur_features[0] = pred
    return preds

def sarimax_forecast(series, steps=7):
    # fit a simple SARIMAX(1,0,1) model
    model = SARIMAX(series, order=(1,0,1), seasonal_order=(0,0,0,0), enforce_stationarity=False, enforce_invertibility=False)
    res = model.fit(disp=False)
    fc = res.get_forecast(steps=steps)
    return fc.predicted_mean, fc.conf_int()

def create_pdf_report(city, outputs, github_url, out_pdf):
    c = canvas.Canvas(out_pdf, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height-40, f"Weather Capstone Report - {city}")
    c.setFont('Helvetica', 10)
    c.drawString(40, height-60, "Objectives:")
    text = c.beginText(40, height-80)
    objectives = [
        '1. Fetch live weather data from API and store in PostgreSQL.',
        '2. Create databases and tables in PostgreSQL.',
        '3. Visualize weather data for a single city (last 30 days).',
        '4. Use ML models for simple forecasting (RandomForest, SARIMAX).',
    ]
    for o in objectives:
        text.textLine(o)
    c.drawText(text)
    c.drawString(40, height-180, f"GitHub URL: {github_url}")
    y = height-200
    for img in outputs:
        if os.path.exists(img):
            c.drawImage(img, 40, y-200, width=520, preserveAspectRatio=True, mask='auto')
            y -= 210
            if y < 120:
                c.showPage()
                y = height-40
    c.save()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', required=True)
    parser.add_argument('--days', type=int, default=30)
    parser.add_argument('--forecast_days', type=int, default=7)
    parser.add_argument('--output', default='report_output')
    parser.add_argument('--github_url', default='GITHUB_REPO_URL_HERE')
    args = parser.parse_args()

    df = get_last_n_days(args.city, args.days)
    if df.empty:
        print('No data found for the city and range. Exiting.')
        return
    os.makedirs(args.output, exist_ok=True)
    # plot temperature and humidity
    temp_png = plot_series(df, args.city, 'temperature_c', os.path.join(args.output, 'temp'))
    hum_png = plot_series(df, args.city, 'humidity', os.path.join(args.output, 'hum'))

    # Forecast with RandomForest
    rf_preds = rf_forecast(df, steps=args.forecast_days, column='temperature_c')

    # Forecast with SARIMAX
    sarimax_preds, conf_int = sarimax_forecast(df['temperature_c'], steps=args.forecast_days)

    # Plot forecast
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df.index[-240:], df['temperature_c'].iloc[-240:], label='Historical (last 240 points)')
    future_idx = [df.index[-1] + timedelta(hours=i+1) for i in range(args.forecast_days)]
    ax.plot(future_idx, rf_preds, marker='o', linestyle='--', label='RF forecast')
    ax.plot(future_idx, sarimax_preds, marker='x', linestyle='--', label='SARIMAX forecast')
    ax.set_title(f"Temperature forecast for {args.city}")
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    forecast_png = os.path.join(args.output, f'forecast_{args.city.replace(' ','_')}.png')
    fig.savefig(forecast_png, bbox_inches='tight')
    plt.close(fig)

    outputs = [temp_png, hum_png, forecast_png]
    pdf_path = os.path.join(args.output, f'report_{args.city.replace(" ","_")}.pdf')
    create_pdf_report(args.city, outputs, args.github_url, pdf_path)
    print('Report generated at', pdf_path)

if __name__ == '__main__':
    main()
