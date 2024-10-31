#!/usr/bin/env python3
import time
import board
from adafruit_seesaw.seesaw import Seesaw
from globals import glo

def initialize():
    global i2c_bus, ss
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)
    print("Soil moisture sensor initialized")

def read_sensor():
    global ss
    try:
        moisture = ss.moisture_read()
        temp = ss.get_temp()
        return moisture, temp
    except Exception as error:
        print(f"Error reading soil sensor: {error}")
        return None, None

def run():
    moisture, temp = read_sensor()
    if moisture is not None and temp is not None:
        print(f"temp: {temp}  moisture: {moisture}")
        glo.realMoist = moisture
    return moisture, temp

def cleanup():
    print("Soil moisture sensor cleaned up")

if __name__ == "__main__":
    initialize()
    try:
        while True:
            run()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSoil moisture sensor monitoring terminated by user")
    finally:
        cleanup()
