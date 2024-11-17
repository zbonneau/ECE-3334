#!/usr/bin/env python3
from globals import glo, DEBUG, VAPORIZER, VAPORIZERRUNTIME
import RPi.GPIO as GPIO
from time import sleep

# Configuration - Add this to globals.py
# VAPORIZER =   # Example GPIO pin
# VAPORIZERRUNTIME = 2  # Example runtime in seconds

def initialize() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(VAPORIZER, GPIO.OUT)
    GPIO.output(VAPORIZER, GPIO.LOW)
    if DEBUG:
        print("Vaporizer initialized")

def run() -> None:
    if glo.realHumd is not None and glo.realHumd < glo.humdMin:
        GPIO.output(VAPORIZER, GPIO.HIGH)
    else:
        GPIO.output(VAPORIZER, GPIO.LOW)
            

def test():
    while True:
        try:
            message = input("RUN or Ctrl+C to quit")
            GPIO.output(VAPORIZER, GPIO.HIGH)
            sleep(VAPORIZERRUNTIME)
            GPIO.output(VAPORIZER, GPIO.LOW)
        except KeyboardInterrupt as error:
            print("End")
            GPIO.output(VAPORIZER, GPIO.LOW)
            return

def cleanup() -> None:
    GPIO.output(VAPORIZER, GPIO.LOW)
    GPIO.cleanup(VAPORIZER)
    if DEBUG:
        print("Vaporizer cleaned up")

if __name__ == "__main__":
    initialize()
    test()
    cleanup()
