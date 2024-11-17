from globals import glo, HOUSEPARAMS, GET_DATA_QUERY, DATASIZE, SEND_DATA_QUERY, DEBUG, VERBOSE
from socket import socket
from DBFunc import parseData, DBSearch, DBInsert
from HouseParameters import GetHouseParams, SetHouseParams
from datetime import datetime

def handleData(con: socket, data: str)->None:
    
    if data.startswith("get_config"):
        try:
            params = parseData(data, 1)
            if params:
                houseID:int = int(params[0])
                config = get_config(houseID)
                set_config(con, config)

        except ValueError as error:
            print(f"get_config parse failed: {error}")
            return
        
        except IndexError as error:
            print(f"get_config parse failed: {error}")
            return
        
        except TypeError as error:
            print(f"get_config parse failure: {error}")
        
    elif data.startswith("send_config"):
        try:
            PiConfig = parseData(data, HOUSEPARAMS)
            if PiConfig is None:
                print("Pi Config parse failed")
                return
            DBConfig = GetHouseParams(glo.path, int(PiConfig[0]))
            if DBConfig is None:
                DBInsert(glo.path, "INSERT INTO HouseConfig VALUES(?,?,?,?,?,?,?,?)", PiConfig)
                get_data(con, int(PiConfig[0]))
            elif PiConfig[7] >= DBConfig[7]:
                params = (
                    float(PiConfig[1]),
                    float(PiConfig[2]),
                    float(PiConfig[3]),
                    float(PiConfig[4]),
                    float(PiConfig[5]),
                    float(PiConfig[6]),
                    PiConfig[7]
                )
                print(SetHouseParams(glo.path, int(PiConfig[0]), params))
                get_data(con, int(PiConfig[0]))
            else:
                set_config(con, DBConfig)

        except ValueError as error:
            print(f"get_config failed: {error}")
            return

    elif data.startswith("send_data"):
        params:tuple = parseData(data, DATASIZE)
        try:
            paramsFormat:tuple = (
                params[1],
                int(params[0]),
                float(params[2]),
                float(params[3]),
                float(params[4]),
            )
            DBInsert(glo.path, SEND_DATA_QUERY, paramsFormat)

        except ValueError as error:
            print(f"send_data parse error: {error}")
            return
    else:
        print(f"error: Unknown network command: {data}")
        raise SyntaxError("Unkown network command. Possibly alien client")

def get_config(houseID: int)->tuple[str]:
    try:
        config = GetHouseParams(glo.path, houseID)
    except Exception as error:
        print(f"get_config failed: {error}")
        return None
    if config is None:
        print(f"No config for house {houseID}")
    return config
                       
def set_config(con:socket, config: tuple[str])->None:
    if config is None:
        return
    try:
        message:str = f"set_config HOUSEID: {int(config[0])}, TEMPMIN: {float(config[1])}, TEMPMAX: {float(config[2])}, HUMDMIN: {float(config[3])}, HUMDMAX: {float(config[4])}, MOISTMIN: {float(config[5])}, MOISTMAX: {float(config[6])}, TIMESTAMP: {config[7]}"
        if VERBOSE:
            print(f"server >{message}")
        con.send(message.encode())  
    except Exception as error:
        print(f"set_config failed: {error}")
        
def get_data(con:socket, houseID: int)->None:
    TimeStamps:tuple[str] = DBSearch(glo.path, GET_DATA_QUERY, (houseID,))
    if TimeStamps is not None and TimeStamps.__len__() >0:
        message = f"get_data HOUSEID: {houseID}, TIMESTAMP: {TimeStamps[0][0]}"
    else:
        message = f"get_data HOUSEID: {houseID}, TIMESTAMP: 0000-00-00 00:00"
    
    if VERBOSE:
        print(f"server >{message}")
    con.send(message.encode())

def serverMain()->None:
    
    host = '0.0.0.0'
    port = glo.port

    glo.server = socket()
    try:
        glo.server.bind((host,port))
        glo.server.settimeout(10)
    except Exception as error:
        print(f"Server Init failed: {error}")
        return
    
    
    while 1:
        
        glo.server.listen(1)

        try:
          glo.con, addr = glo.server.accept()

        except TimeoutError:
            if (DEBUG):
                print("Server TimeOut")
            continue
        
        print(f"\nNew Connection: pi@{addr[0]} | {datetime.now().isoformat(sep=' ', timespec='minutes')}")
        buffer = ""
        while True:
            try:
                data = glo.con.recv(1024).decode()
                buffer += data # buffer data b/c TCP stream does not delimit messages
                if not data:
                    break
                else:
                    while '\n' in buffer: 
                        line, buffer = buffer.split('\n', 1)
                        if VERBOSE:
                            print(f"pi@{addr[0]} >{line}")
                        handleData(glo.con, line)

            except Exception as error:
                print(error)
                break

        glo.closeCon()


if __name__ == "__main__":
    try:
        serverMain()
    except KeyboardInterrupt:
        if (DEBUG):
            print("Server Terminated by user (CTL+C)")
        glo.closeCon()
        glo.closeServer()