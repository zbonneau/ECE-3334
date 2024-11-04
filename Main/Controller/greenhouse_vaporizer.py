#!/usr/bin/env python3
import serial
import time
from globals import glo, DEBUG

# Configuration
VAPORIZER_PORT = '/dev/ttyUSB0'  # Common USB port on Linux/Raspberry Pi
BAUD_RATE = 9600

def initialize():
    global vaporizer
    try:
        vaporizer = serial.Serial(VAPORIZER_PORT, BAUD_RATE)
        if DEBUG:
            print("Vaporizer initialized")
        time.sleep(2)  # Wait for device to initialize
    except serial.SerialException as e:
        print(f"Error initializing vaporizer: {e}")
        raise

def turn_on():
    try:
        vaporizer.write(b'ON\n')  # Example command
        if DEBUG:
            print("Vaporizer turned ON")
    except serial.SerialException as e:
        print(f"Error controlling vaporizer: {e}")

def turn_off():
    try:
        vaporizer.write(b'OFF\n')  # Example command
        if DEBUG:
            print("Vaporizer turned OFF")
    except serial.SerialException as e:
        print(f"Error controlling vaporizer: {e}")

def run():
    if glo.realHumd is not None:
        if glo.realHumd < glo.humdMin:
            turn_on()
        elif glo.realHumd > glo.humdMax:
            turn_off()

def cleanup():
    if 'vaporizer' in globals():
        vaporizer.close()
    print("Vaporizer cleaned up")

if __name__ == "__main__":
    initialize()
    try:
        while True:
            run()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nVaporizer control terminated by user")
    finally:
        cleanup()
