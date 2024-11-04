#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from globals import glo, WATER_SENSOR_PIN, DEBUG

# Configuration
# WATER_SENSOR_PIN = 17  # GPIO17
CHECK_INTERVAL = 5  # seconds

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WATER_SENSOR_PIN, GPIO.IN)
    if DEBUG:
        print("Water sensor initialized")

def read_sensor():
    return GPIO.input(WATER_SENSOR_PIN)

def run():
    water_detected = read_sensor()
    if DEBUG:
        if water_detected:
            print("Water detected!")
        else:
            print("No water detected.")
    return water_detected

def cleanup():
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup(WATER_SENSOR_PIN)
    if DEBUG:
        print("Water sensor cleaned up")

if __name__ == "__main__":
    initialize()
    try:
        while True:
            run()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nWater sensor monitoring terminated by user")
    finally:
        cleanup()
