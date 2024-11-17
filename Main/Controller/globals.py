import RPi.GPIO as GPIO
import board
import configparser
from datetime import datetime
import adafruit_dht as dht
from socket import socket, SHUT_RDWR
import sqlite3 as sql
from sys import argv

DHT_PIN = board.D4  # GPIO4
PUMP        = 27
PUMPRUNTIME = 2
VAPORIZER   = 22  # GPIO 
VAPORIZERRUNTIME = 20  # seconds
WATER_SENSOR_PIN = 17  # GPIO17
CHECK_INTERVAL = 30  # seconds
FAN_PIN    = 14
CONFIGPATH = "config.ini"
DEBUG      = False
DEBUGCOMMS = True
PORT       = 5000
IP         = "10.131.16.152" # local host for dev
HOUSEPARAMS = 8
PATH = "prod.db"
POLLINTERVAL = 15 # interval in minutes between house reads 
MAXATTEMPTS = 3 # Maximum attempts to connect socket during poll

def DBInitData(path:str)->None:
    try:
        DATA_TABLE_CREATE = """
            CREATE TABLE IF NOT EXISTS data(
            TIMESTAMP TEXT,
            HOUSEID   INTEGER,                          
            TEMP      REAL,
            HUMIDITY  REAL,
            MOISTURE  REAL
            );
            """ 
        con = sql.connect(path)
        con.execute(DATA_TABLE_CREATE)
        con.execute("INSERT INTO data VALUES(?, 0, 0, 0, 0);", ("0000-00-00 00:00",))
        con.commit()
        con.close()
        
    except sql.Error as error:
        print(f"Data Table Init Failed: {error}")

class Global:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIGPATH)
        self.config.sections()

        try:
            self.houseID:   int     = self.config.getint("HouseParams",   "HouseID", fallback=0)
            self.tempMin:   float   = self.config.getfloat("HouseParams", "TempMin")
            self.tempMax:   float   = self.config.getfloat("HouseParams", "TempMax")
            self.humdMin:   float   = self.config.getfloat("HouseParams", "HumdMin")
            self.humdMax:   float   = self.config.getfloat("HouseParams", "HumdMax")
            self.moistMin:  float   = self.config.getfloat("HouseParams", "MoistMin")
            self.moistMax:  float   = self.config.getfloat("HouseParams", "MoistMax")
            self.timeStamp: str     = self.config["HouseParams"]["TimeStamp"]
            self.soilMin:   float   = self.config.getfloat("SoilSensor", "sensorMin", fallback=300)
            self.soilMax:   float   = self.config.getfloat("SoilSensor", "sensorMax", fallback=1000)
            self.realTemp:  float   = None
            self.realHumd:  float   = None
            self.realMoist: float   = None   
            self.closeApplication = False # set true by top script to end threads safely 

        except ValueError as error:
            print(f"Startup Failed: {error}")
            return 

        message =   "===== STARTUP ==================\n"
        message += f"  HOUSEID: {self.houseID}\n"
        message += f"  TEMP  MIN/MAX: {self.tempMin:.1f}:{self.tempMax:.1f}\n"
        message += f"  HUMD  MIN/MAX: {self.humdMin:.1f}:{self.humdMax:.1f}\n"
        message += f"  MOIST MIN/MAX: {self.moistMin:.1f}:{self.moistMax:.1f}\n"
        message += f"  TIMESTAMP: {self.timeStamp}\n"
        print(message)
        
        self.dht_device: dht.DHT22 = None

        self.socket:socket = None
        self.IP = IP
        if argv.__len__() >1:
            self.IP = argv[1]
        self.path = PATH

        DBInitData(PATH)
        
    
    def saveConfig(self)->None:
        self.config.set('HouseParams', 'TempMin',   self.tempMin.__str__())
        self.config.set('HouseParams', 'TempMax',   self.tempMax.__str__())
        self.config.set('HouseParams', 'HumdMin',   self.humdMin.__str__())
        self.config.set('HouseParams', 'HumdMax',   self.humdMax.__str__())
        self.config.set('HouseParams', 'MoistMin',  self.moistMin.__str__())
        self.config.set('HouseParams', 'MoistMax',  self.moistMax.__str__())
        self.config.set('HouseParams', 'TimeStamp', self.timeStamp)

        with open(CONFIGPATH, 'w') as file:
            self.config.write(file)

    def editConfig(self, params:tuple)->bool:   
        if (self.houseID != params[0]):
            return False
        if (params.__len__() != 8):
            return False
        try:
            self.tempMin    = params[1]
            self.tempMax    = params[2]
            self.humdMin    = params[3]
            self.humdMax    = params[4]
            self.moistMin   = params[5]
            self.moistMax   = params[6]
            self.timeStamp  = params[7]
            if DEBUG or DEBUGCOMMS:
                message =   "===== CONFIG EDIT ==================\n"
                message += f"  HOUSEID: {self.houseID}\n"
                message += f"  TEMP  MIN/MAX: {self.tempMin:.1f}:{self.tempMax:.1f}\n"
                message += f"  HUMD  MIN/MAX: {self.humdMin:.1f}:{self.humdMax:.1f}\n"
                message += f"  MOIST MIN/MAX: {self.moistMin:.1f}:{self.moistMax:.1f}\n"
                message += f"  TIMESTAMP: {self.timeStamp}\n"
            self.saveConfig()
            return True
        
        except Exception as error:
            if DEBUG:
                print(f"editConfig error: {error}")
            return False

    def closeSocket(self)->None:
        if not glo.socket:
            return
        try:
            glo.socket.shutdown(SHUT_RDWR)
            glo.socket.close()
            glo.socket = None
        
        except Exception as error:
            if DEBUG:
                print(f"globals.py::closeSocket() > {error}")

glo = Global()
