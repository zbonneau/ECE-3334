# Communication system
 cmd oneliner
 - <path\to\dir>\env\scripts\activate && cd <path\to\dir>\main\monitor && python MonitorComms.py
 - C:\Users\Zack\ECE-3334\env\scripts\activate && cd C:\Users\Zack\ECE-3334\main\monitor && python MonitorComms.py

## Connection sequence - Monitor
1. Power on Pi
2. Establish SSH

Loop
3. Listen for Connection - Accept
4. case(recv):
    - get_config(HouseID): send(set_config SQL(SELECT CONFIG WHERE houseID = recv))
    - send_config(Config): if (recv(config.Timestamp) >= SQL(CONFIG).TimeStamp):
        - T: update SQL Config, break
        - F: send(set_config SQL(Config))
    - reject_config(): Warn User, break 4
5. send(get_data SQL(SELECT DATETIME FROM Data WHERE HouseID = config, orderby DATETIME).fetchone or None)
6. while connection is open:  SQL(INSERT recv(send_data(DATA)))

## Connection Sequence - Controller
1. Power on Pi
2. Establish SSH
3. Connect to Monitor

Loop
4. Config.ini has values
    - N: send(get_config(HouseID))
    - Y: send(send_config(config))
5. case(recv)
    - set_config(config): is valid?
        - N: send(reject Config)
        - Y: is recv.config.timeStamp newer than config.ini?
            - Y: update config
        - send(send_config)
    - get_data(Timestamp)
        - data = SQL(SELECT * FROM data WHERE DATETIME > TimeStamp ORDERBY DATETIME).fetchall()
        - send(send_data Data) for Data in data
        - close connection
        - SQL(DELETE FROM data WHERE DATETIME <= TimeStamp)

6. Every {Time Interval}: Capture Data
7. if (open connection):
    - Y: Loop
    - N: SQL(Insert Data into data), loop 6

## Communication commands - Monitor
### set_config HOUSEID:int, TEMPMIN: float, TEMPMAX: float, HUMDMIN: float, HUMDMAX:float, MOISTMIN: float, MOISTMAX: float, TIMESTAMP: str

### get_data HOUSEID: int, TIMESTAMP: str

## Communication commands - Controller
### get_config HOUSEID: int

### send_config HOUSEID: int, TEMPMIN: float, TEMPMAX: float, HUMDMIN: float, HUMDMAX:float, MOISTMIN: float, MOISTMAX: float, TIMESTAMP: str

### reject_config Error: str

### send_data HOUSEID:int, TIMESTAMP: str, TEMP: float, HUMD: float, MOIST: float

