import socket
import threading
import sqlite3 as sql
from DBFunc import DBSearch
DEBUG = False
TEMP_MIN_ABS = 0
TEMP_MAX_ABS = 100
HUMD_MIN_ABS = 0
HUMD_MAX_ABS = 100
MOIST_MIN_ABS = 0
MOIST_MAX_ABS = 100
DBPATH = "Main\\Monitor\\test.db"
PORT = 5000
HOUSEPARAMS = 8
GET_DATA_QUERY = """
SELECT TIMESTAMP FROM data 
WHERE HOUSEID = ?
ORDER BY TIMESTAMP DESC
;
"""
SEND_DATA_QUERY = """
INSERT INTO data VALUES(?,?,?,?,?);"""
DATASIZE = 5

HOUSECONFIG_CREATE = """
CREATE TABLE IF NOT EXISTS HouseConfig(
HOUSEID   INTEGER,
TEMPMIN   REAL,
TEMPMAX   REAL,
HUMDMIN   REAL,
HUMDMAX   REAL,
MOISTMIN  REAL,
MOISTMAX  REAL,
TIMESTAMP TEXT);
""" # Create table plus dummy entry 

DATA_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS data(
TIMESTAMP TEXT,
HOUSEID   INTEGER,                          
TEMP      REAL,
HUMIDITY  REAL,
MOISTURE  REAL
);
""" # 

## moved to globals.py to prevent circular dependency
def DBInitConfig(path:str)->None:
    try:
        con = sql.connect(path)
        con.execute(HOUSECONFIG_CREATE)
        con.execute("INSERT INTO HouseConfig VALUES(0,0,100,0,100,0,100,?); ", ("0000-00-00 00:00",))
        con.commit()
        con.close()
        
    except sql.Error as error:
        print(f"House Config Table Init Failed: {error}")

def DBInitData(path:str)->None:
    try:
        con = sql.connect(path)
        con.execute(DATA_TABLE_CREATE)
        con.execute("INSERT INTO data VALUES(?, 0, 0, 0, 0);", ("0000-00-00 00:00",))
        con.commit()
        con.close()
        
    except sql.Error as error:
        print(f"Data Table Init Failed: {error}")

class globals:
    def __init__(self):
        self.con: socket.socket = None
        self.server: socket.socket = None
        self.path:str = DBPATH
        self.port:int = PORT

        exists = DBSearch(self.path, "SELECT DISTINCT HOUSEID FROM HouseConfig", None)
        if not exists:
            DBInitConfig(self.path)
        
        exists = DBSearch(self.path, "SELECT DISTINCT HOUSEID FROM data", None)
        if not exists:
            DBInitData(self.path)


    def closeServer(self):
        if self.server:
            self.server.close()

    def closeCon(self):
        if self.con:
            self.con.close()
        
        

glo:globals = globals()

