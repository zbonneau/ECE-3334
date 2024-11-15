from globals import glo, PUMP, PUMPRUNTIME
import RPi.GPIO as GPIO
from time import sleep

def initialize()->None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.output(PUMP, GPIO.LOW)
    print("PUMP initialized")

def run()->None:
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
    GPIO.cleanup()

if __name__ == "__main__":
    
    initialize()
    test()
    cleanup()