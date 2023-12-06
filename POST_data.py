import requests
import json
from datetime import datetime
import Adafruit_DHT

current_datetime = datetime.now()
date_time = current_datetime
formatted_datetime = date_time.strftime('%Y-%m-%d %H:%M:%S')
truncated_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')

print(truncated_datetime)

temperature_unit = 'C'

sensor = Adafruit_DHT.DHT11
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

date_time_str = truncated_datetime.strftime('%Y-%m-%d %H:%M:%S')

data = {'date_time': date_time_str,
        'temperature': temperature,
        'humidity': humidity,
        'temperature_unit': temperature_unit}  # Your JSON data
url = 'http://valthefirst.pythonanywhere.com/new'  # Replace with your app's URL

response = requests.post(url, json=data)

if response.status_code == 200:
    print("JSON data sent successfully!")
else:
    print("Failed to send JSON data:", response.status_code)
