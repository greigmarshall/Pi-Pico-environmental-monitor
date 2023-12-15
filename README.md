# Pi-Pico-environmental-monitor

## Introduction
This repo is a familiarisation exercise with GitHub, and its version control, planning and documentation tools.

The project itself is code I wrote with extensive help from ChatGPT a while ago. It uses MicroPython to control a [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) which has a [DHT20](https://www.adafruit.com/product/5183) sensor and a simple light dependent resistor (LDR) circuit attached. The system takes readings from the sensors every minute, and submits them to an MQTT broker. [Home Assistant](https://www.home-assistant.io/) is subscribed to the appropriate topics and can parse the data for logical operations (turn a light on if it's dark etc.)

Each sensor platform has a BOM of about £20 including its Pico, USB cable, breadboard, header pins, sensors and jumper wires. They can be used to control a smart home, and are easily modified to add or replace sensor types. Using MQTT, they are not dependent on any proprietary smart home system such as Ikea [Trådfri](https://www.ikea.com/gb/en/product-guides/ikea-home-smart-system/) or [Philips Hue](https://www.philips-hue.com/en-gb), but using Home Assistant can push information out to Apple Home or Google equivalents. 

## Aims
The code was previously kept in a local Bookstack instance, but this has no version control etc. I intend to keep the code here, improve on it, and document its development, functionality and improvement.

## Plans
The system runs well- months at a time when the MQTT broker is constantly available. When the MQTT broker is unavailable however (due to a reboot or the WLAN dropping), the system fails to recover from the interruption and remains offline pending a restart. This should be easy to investigate and fix, but it's the documentation of this process that is important. 
