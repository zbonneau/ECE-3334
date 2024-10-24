#!/usr/bin/env python3
import time
import board
import adafruit_dht

# Configuration
DHT_PIN = board.D4  # GPIO4
READ_INTERVAL = 2  # seconds

# Global variables
dht_device = None
last_read_time = 0

def initialize():
    global dht_device
    dht_device = adafruit_dht.DHT22(DHT_PIN)
    print("DHT22 sensor initialized")

def read_sensor():
    global last_read_time
    current_time = time.time()
    
    if current_time - last_read_time >= READ_INTERVAL:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            last_read_time = current_time
            return temperature, humidity
        except RuntimeError as error:
            print(f"Error reading DHT22 sensor: {error.args[0]}")
    
    return None, None

def run():
    temperature, humidity = read_sensor()
    if temperature is not None and humidity is not None:
        print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
    else:
        print("Waiting for valid sensor reading...")

def cleanup():
    global dht_device
    if dht_device:
        dht_device.exit()
    print("DHT22 sensor cleaned up")

if __name__ == "__main__":
    initialize()
    try:
        while True:
            run()
            time.sleep(READ_INTERVAL)
    except KeyboardInterrupt:
        print("\nDHT22 sensor monitoring terminated by user")
    finally:
        cleanup()
