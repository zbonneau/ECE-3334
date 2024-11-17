#!/usr/bin/env python3
import time
import board
from adafruit_seesaw.seesaw import Seesaw
from globals import glo, DEBUG

# Zachary Bonneau 11/13/2024 @ 7 PM
# From Pi testing:
#   air = 300-400
#   dirt = 400-500
#   damp = 500-600
#   mud  = 600-700
#   water = 700+



#  new values water = 1000
# For %:
#   0% = 300
# 100% = 700
# moist = (reading - 300) / 400 * 100%

def initialize():
    global i2c_bus, ss
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)
    if DEBUG:
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
    
def scaleMoisture(moisture:int)->float:
    if moisture < glo.soilMin:
        return 0 # 0%
    if moisture > glo.soilMax:
        return 100 # 100 %
    return (moisture - glo.soilMin) * (100/(glo.soilMax-glo.soilMin)) # Linear scale 300-700 = 0% 100%

def run():
    moistureSum:int = 0
    for _ in range(20): # Take avg of 20 readings
        moisture, temp = read_sensor()
        moistureSum += moisture

    moisture = moistureSum / 20
    if moisture is not None and temp is not None and DEBUG:
        print(f"temp: {temp:.1f}  moisture: {moisture}")
    glo.realMoist = scaleMoisture(moisture)
    return moisture, temp

def cleanup():
    if DEBUG:
        print("Soil moisture sensor cleaned up")

if __name__ == "__main__":
    initialize()
    DEBUG = True
    try:
        while True:
            run()
            print(f"scaled moisture: {glo.realMoist}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSoil moisture sensor monitoring terminated by user")
    finally:
        cleanup()
