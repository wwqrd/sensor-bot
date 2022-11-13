#!/usr/bin/env python

import time
import datetime
import os
import sys
import bme680
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY = os.environ["ADAFRUIT_IO_KEY"]
ADAFRUIT_IO_USERNAME = os.environ["ADAFRUIT_IO_USERNAME"]

print("v3", flush=True)

def connected(client):
    print('Connected.', flush=True)

def disconnected(client):
    print('Disconnected.', flush=True)
    sys.exit(1)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected

client.connect()

while True:
    print(datetime.datetime.now(), flush=True, end=": ")
    if sensor.get_sensor_data():
        temperature, pressure, humidity = sensor.data.temperature, sensor.data.pressure, sensor.data.humidity

        client.publish('temperature', temperature)
        client.publish('pressure', pressure)
        client.publish('humidity', humidity)

        output = '{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
            temperature,
            pressure,
            humidity)
        print(output, flush=True)
    time.sleep(30)
