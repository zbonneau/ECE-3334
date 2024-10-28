import board
import configparser
from datetime import datetime
import adafruit_dht as dht

DHT_PIN = board.D4  # GPIO4
WATER_SENSOR_PIN = 17  # GPIO17
# CHECK_INTERVAL = 5  # seconds
FAN_PIN = 14
CONFIGPATH = "config.ini"

class Global:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIGPATH)
        config.sections()

        try:
            self.HouseID:   int     = config.getint("HouseParams", "HouseID", fallback=0)
            self.tempMin:   float   = config.getfloat("HouseParams", "TempMin")
            self.tempMax:   float   = config.getfloat("HouseParams", "TempMax")
            self.humdMin:   float   = config.getfloat("HouseParams", "HumdMin")
            self.humdMax:   float   = config.getfloat("HouseParams", "HumdMax")
            self.moistMin:  float   = config.getfloat("HouseParams", "MoistMin")
            self.moistMax:  float   = config.getfloat("HouseParams", "MoistMax")
            self.timeStamp: str     = config["HouseParams"]["TimeStamp"]
            self.realTemp:  float   = None
            self.realHumd:  float   = None
            self.realMoist: float   = None

        except ValueError as error:
            print(f"Startup Failed: {error}")
            return 
        
        self.dht_device: dht.DHT22 = None
    
    def saveConfig(self)->None:
        pass

    def editConfig(self, params:tuple)->bool:
        pass

glo = Global()