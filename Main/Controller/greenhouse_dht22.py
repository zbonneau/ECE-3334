#!/usr/bin/env python3
import time
import board
import adafruit_dht
from globals import glo, DHT_PIN, DEBUG

# Configuration
# DHT_PIN = board.D4  # GPIO4
READ_INTERVAL = 2  # seconds

# Global variables
# dht_device = None
last_read_time = 0

def initialize():
    glo.dht_device = adafruit_dht.DHT22(DHT_PIN)
    if DEBUG:
        print("DHT22 sensor initialized")

def read_sensor():
    global last_read_time
    current_time = time.time()
    
    if current_time - last_read_time >= READ_INTERVAL:
        try:
            glo.dht_device.measure()
            temperature = glo.dht_device.temperature
            humidity = glo.dht_device.humidity
            last_read_time = current_time
            return temperature, humidity
        except RuntimeError as error:
            print(f"Error reading DHT22 sensor: {error.args[0]}")
    
    return None, None

def run():
    glo.realTemp, glo.realHumd = read_sensor()
    if DEBUG:    
        if glo.realTemp is not None and glo.realHumd is not None:
            print(f"Temperature: {glo.realTemp:.1f}°C, Humidity: {glo.realHumd:.1f}%")
        else:
            print("Waiting for valid sensor reading...")

def cleanup():
    if glo.dht_device:
        glo.dht_device.exit()
        if DEBUG:
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
