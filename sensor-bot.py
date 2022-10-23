#!/usr/bin/env python

import time
import bme680
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY = 'YOUR KEY'
ADAFRUIT_IO_USERNAME = 'USERNAME'

def connected(client):
    print('Connected to Adafruit IO')

def disconnected(client):
    print('Disconnected from Adafruit IO')
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

client.loop_background()

try:
    while True:
        if sensor.get_sensor_data():
            output = 'Sensor reading: {0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
                sensor_data.temperature,
                sensor_data.pressure,
                sensor_data.humidity)
            print(output)
            client.publish('temperature', sensor_data.temperature)
            client.publish('pressure', sensor_data.pressure)
            client.publish('humidity', sensor_data.humidity)

        time.sleep(10)
