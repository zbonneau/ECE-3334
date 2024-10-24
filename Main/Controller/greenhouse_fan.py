#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
FAN_PIN = 14
TEMP_MIN = 15.5  # 60°F
TEMP_MAX = 26.7  # 80°F
HUMIDITY_MAX = 60.0

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    print("Fan control initialized")

def run(temperature, humidity):
    if temperature is not None and humidity is not None:
        print(f"Fan control - Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        
        if temperature > TEMP_MAX or humidity > HUMIDITY_MAX:
            GPIO.output(FAN_PIN, GPIO.HIGH)
            print(f"Fan ON (Pin: {FAN_PIN})")
        elif temperature < TEMP_MIN and humidity < HUMIDITY_MAX - 5:
            GPIO.output(FAN_PIN, GPIO.LOW)
            print(f"Fan OFF (Pin: {FAN_PIN})")
    else:
        print("Fan control - Waiting for valid sensor reading...")

def cleanup():
    GPIO.cleanup()
    print("Fan control cleaned up")

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
