import json
from machine import Pin, I2C
from utime import sleep
from dht20 import DHT20
from umqtt.simple import MQTTClient
import network
from netcredentials import *

# Set up the Wi-Fi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait for the connection to be established
led = machine.Pin("LED", machine.Pin.OUT)
while not wifi.isconnected():
    led.on()  # Turn on the LED
    sleep(0.166)  # Blink at a rate of 3Hz (0.166 seconds on, 0.166 seconds off)
    led.off()  # Turn off the LED
    sleep(0.166)

# Connection established
led.off()  # Turn off the LED
print("Connected to Wi-Fi")

# Set up the MQTT client
mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=MQTT_KEEPALIVE)

i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

dht20 = DHT20(0x38, i2c0)

# Initialize analog input pin
adc_pin = machine.Pin(26, machine.Pin.IN)
prev_val = 0

while True:
    try:
        try:
            # Read analog value from ADC pin
            adc = machine.ADC(26)
            val = adc.read_u16()
            mapped_val = int(val * 1023 / 65535)
            prev_val = mapped_val
        except:
            mapped_val = prev_val
            continue
            
        measurements = dht20.measurements
        data = {
            "temperature": measurements['t'],
            "humidity": measurements['rh'],
            "illuminance": mapped_val
        }
        payload = json.dumps(data)
        print(payload)
        mqtt_client.connect()
        mqtt_client.publish(MQTT_TOPIC, payload)
        mqtt_client.disconnect()
    except OSError:
        print("Failed to read DHT20 sensor")

    sleep(30)
