import datetime
import time
import daemon
import RPi.GPIO as GPIO
import subprocess
import requests
import json
from datetime import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO

# Time setup
current_datetime = datetime.now()
date_time = current_datetime
formatted_datetime = date_time.strftime('%Y-%m-%d %H:%M:%S')
truncated_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')
date_time_str = truncated_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Set GPIO mode and pins
GPIO.setmode(GPIO.BCM)
TRIG1 = 26  # GPIO pin for the sensor's trigger
ECHO1 = 4  # GPIO pin for the sensor's echo

TRIG2 = 27  # GPIO pin for the sensor's trigger
ECHO2 = 22  # GPIO pin for the sensor's echo

middle = 40

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)


# Temperature setup
temperature_unit = 'C'
sensor = Adafruit_DHT.DHT11
pin = 21
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# JSON setup
data = {'date_time': date_time_str,
        'temperature': temperature,
        'humidity': humidity,
        'temperature_unit': temperature_unit}
url = 'http://valthefirst.pythonanywhere.com/new'


def distance(trig_pin, echo_pin):
    # Function to calculate distance using ultrasonic sensor
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    dist = (elapsed_time * 34300) / 2  # Speed of sound is 343 m/s

    return dist
    
    
def post_data():
    # Setup
    # Time setup
    current_datetime = datetime.now()
    date_time = current_datetime
    formatted_datetime = date_time.strftime('%Y-%m-%d %H:%M:%S')
    truncated_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')
    date_time_str = truncated_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Temperature setup
    temperature_unit = 'C'
    GPIO.setmode(GPIO.BCM)
    sensor = Adafruit_DHT.DHT11
    pin = 21
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # JSON setup
    data = {'date_time': date_time_str,
            'temperature': temperature,
            'humidity': humidity,
            'temperature_unit': temperature_unit}
    url = 'http://valthefirst.pythonanywhere.com/new'

    # POST request to a database on the cloud
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Temperature data sent successfully!")
    else:
        print("Failed to send temperature data:", response.status_code)


def main_program():
    while True:
        dist1 = distance(TRIG1, ECHO1)
        dist2 = distance(TRIG2, ECHO2)
        middle = 40  
        
        # Check if both sensors detect something
        if dist1 < middle:
            if dist2 < middle:
                with open('/home/nneji/distance.txt', 'a') as fh:
                    fh.write("Person entered the room!\n")  
                    fh.write("POSTING...\n")
                    post_data()
        time.sleep(0.2)
        

with daemon.DaemonContext():
    main_program()
