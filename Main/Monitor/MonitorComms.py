from globals import glo, HOUSEPARAMS, GET_DATA_QUERY, DATASIZE, SEND_DATA_QUERY
from socket import socket
from DBFunc import parseData, DBSearch, DBInsert
from HouseParameters import GetHouseParams, SetHouseParams

def handleData(con: socket, data: str)->None:
    
    if data.startswith("get_config"):
        try:
            houseID:int = int(parseData(data, 1)[0])
            config = get_config(houseID)
            set_config(con, config)

        except ValueError as error:
            print(f"get_config parse failed: {error}")
            return
        
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
                int(params[0]),
                params[1],
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
        message:str = f"send_config HOUSEID: {int(config[0])}, TEMPMIN: {float(config[1])}, TEMPMAX: {float(config[2])}, HUMDMIN: {float(config[3])}, HUMDMAX: {float(config[4])}, MOISTMIN: {float(config[5])}, MOISTMAX: {float(config[6])}, TIMESTAMP: {config[7]}"
        con.send(message.encode())  
    except Exception as error:
        print(f"set_config failed: {error}")
        
def get_data(con:socket, houseID: int)->None:
    TimeStamps:tuple[str] = DBSearch(glo.path, GET_DATA_QUERY, (houseID,))
    if TimeStamps is not None and TimeStamps.__len__() >0:
        con.send(f"get_data HOUSEID: {houseID}, TIMESTAMP: {TimeStamps[0]}".encode())
    else:
        con.send(f"get_data HOUSEID: {houseID}, TIMESTAMP: 0000-00-00 00:00".encode())

def serverMain()->None:
    
    host = '0.0.0.0'
    port = glo.port

    server = socket()
    try:
        server.bind((host,port))
    except Exception as error:
        print(f"Server Init failed: {error}")
        return
    
    while 1:
        server.listen(1)

        glo.con, addr = server.accept()

        while True:
            try:
                data = glo.con.recv(1024).decode()
                if not data:
                    break
                else:
                    handleData(glo.con, data)

            except Exception as error:
                print(error)
                break

        glo.closeCon()


if __name__ == "__main__":
    serverMain()