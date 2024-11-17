#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from globals import glo, FAN_PIN, DEBUG

# Configuration
# FAN_PIN = 14
# glo.tempMin = 15.5  # 60°F
# glo.tempMax = 26.7  # 80°F
# HUMIDITY_MAX = 60.0

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, GPIO.LOW)
    if DEBUG:
        print("Fan control initialized")

def run():
    if glo.realTemp is not None and glo.realHumd is not None:
        if DEBUG:
            print(f"Fan control - Temp: {glo.realTemp:.1f}°C, Humidity: {glo.realHumd:.1f}%")
        
        if glo.realTemp > glo.tempMax or glo.realHumd > glo.humdMax:
            GPIO.output(FAN_PIN, GPIO.HIGH)
            if DEBUG:
                print(f"Fan ON (Pin: {FAN_PIN})")
        elif glo.realTemp < glo.tempMin and glo.realHumd < glo.humdMax - 5:
            GPIO.output(FAN_PIN, GPIO.LOW)
            if DEBUG:
                print(f"Fan OFF (Pin: {FAN_PIN})")
    elif DEBUG:
        print("Fan control - Waiting for valid sensor reading...")

def cleanup():
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.cleanup(FAN_PIN)
    if DEBUG:
        print("Fan control cleaned up")

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
