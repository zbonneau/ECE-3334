from globals import glo, DEBUG, PUMP, PUMPRUNTIME
import RPi.GPIO as GPIO
from time import sleep

def initialize()->None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.output(PUMP, GPIO.LOW)
    if DEBUG:
        print("PUMP initialized")

def run()->None:
    if (glo.realMoist < glo.moistMin):
        GPIO.output(PUMP, GPIO.HIGH)
        sleep(PUMPRUNTIME)
        GPIO.output(PUMP, GPIO.LOW)


def test():
    while True:
        try:
            message = input("RUN or Ctrl+C to quit")
            run()
        except KeyboardInterrupt as error:
            print("End")
            GPIO.output(PUMP, GPIO.LOW)
            return

def cleanup()->None:
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.cleanup(PUMP)

if __name__ == "__main__":
    glo.realMoist = 20
    glo.moistMin = 30
    initialize()
    test()
    cleanup()
