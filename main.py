import json
from machine import Pin, I2C
from utime import sleep
from dht20 import DHT20
from umqtt.simple import MQTTClient
import network

# Configure Wi-Fi and MQTT broker settings
SSID = "SSID"
PASSWORD = "WIFI PASSWORD"
MQTT_BROKER = "BROKER ADDRESS"
MQTT_PORT = 1883
MQTT_USER = "MQTT USER"
MQTT_PASSWORD = "MQTT PASS"
MQTT_TOPIC = "homeassistant/dht20/1"
CLIENT_ID = "pico2"
MQTT_KEEPALIVE = 60

# Set up the Wi-Fi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait for the connection to be established
while not wifi.isconnected():
    sleep(1)

print("Connected to Wi-Fi")

# Set up the MQTT client
mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=MQTT_KEEPALIVE)

i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

dht20 = DHT20(0x38, i2c0)

while True:
    try:
        measurements = dht20.measurements
        data = {
            "temperature": measurements['t'],
            "humidity": measurements['rh']
        }
        payload = json.dumps(data)
        print(payload)
        mqtt_client.connect()
        mqtt_client.publish(MQTT_TOPIC, payload)
        mqtt_client.disconnect()
    except OSError:
        print("Failed to read DHT20 sensor")

    sleep(1)
