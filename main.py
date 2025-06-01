from flask import Flask, render_template
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) # Changed 'app' to __name__ as is standard practice

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/weather')
@app.route('/weather.html')
def weather():
    Weather_API_KEY = os.environ.get("Weather_API_KEY")
    lat = 46.4917  # Sudbury latitude
    lon = -80.9930  # Sudbury longitude
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Weather_API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': 'Sudbury, Canada',
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'pressure': data['main']['pressure'],
                'visibility': round(data.get('visibility', 0) / 1000, 1)  # Convert m to km
            }
            return render_template('weather.html', weather=weather_data)
        else:
            error_message = "Unable to fetch weather data. Please try again later."
            return render_template('weather.html', error=error_message)
    except Exception as e:
        error_message = "An error occurred while fetching weather data. Please try again later."
        return render_template('weather.html', error=error_message)

@app.route('/stock')
@app.route('/stock.html')
def stock():
    Stock_API_KEY = os.environ.get("Stock_API_KEY")
    symbol = "NVDA"  # Default symbol
    
    # Get intraday data
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={Stock_API_KEY}"
    r = requests.get(url)
    intraday_data = r.json()
    
    # Get company overview
    overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={Stock_API_KEY}"
    overview_r = requests.get(overview_url)
    overview_data = overview_r.json()
    
    if "Time Series (5min)" in intraday_data:
        # Get the latest data point
        latest_time = list(intraday_data["Time Series (5min)"].keys())[0]
        latest_data = intraday_data["Time Series (5min)"][latest_time]
        
        stock_data = {
            'symbol': symbol,
            'company_name': overview_data.get('Name', symbol),
            'price': round(float(latest_data['4. close']), 2),
            'change': round(float(latest_data['4. close']) - float(latest_data['1. open']), 2),
            'volume': int(latest_data['5. volume']),
            'high': round(float(latest_data['2. high']), 2),
            'low': round(float(latest_data['3. low']), 2),
            'market_cap': overview_data.get('MarketCapitalization', 'N/A'),
            'pe_ratio': overview_data.get('PERatio', 'N/A'),
            'dividend_yield': overview_data.get('DividendYield', 'N/A'),
            'sector': overview_data.get('Sector', 'N/A'),
            'description': overview_data.get('Description', 'No description available'),
            'last_updated': latest_time
        }
        
        # Calculate percent change
        stock_data['percent_change'] = round((stock_data['change'] / (stock_data['price'] - stock_data['change'])) * 100, 2)
        
        return render_template('stock.html', stock=stock_data)
    else:
        error_message = "Unable to fetch stock data. Please try again later."
        return render_template('stock.html', error=error_message)

if __name__ == '__main__': # Added this block for better practice
    app.run(host='0.0.0.0', port=8080)
