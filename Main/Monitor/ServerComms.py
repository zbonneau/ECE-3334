import socket
import threading
from globals import glo 
from DBFunc import parseData, DBInsert, DBSearch
from HouseParameters import GetHouseParams, SetHouseParams


def handle_client(con:socket.socket):
    while True:
        data = con.recv(1024).decode()
        if not data:
            break

        handle_client_data(con, data)

    con.close()

def handle_client_data(con:socket.socket, data: str)->None:
    global glo
    if data.startswith("send_data"):
        values: tuple[str] = parseData(data, 5)
        if values is None:
            return
        query = """INSERT INTO data VALUES(?,?,?,?,?);"""
        try:
            error: str = DBInsert(glo.path, query, (values[0], int(values[1]), float(values[2]), float(values[3]), float(values[4])))
            if error is not None:
                print(error)
        except ValueError as error:
            print(error)

    elif data.startswith("send_config"):
        values: tuple[str] = parseData(data, 7)
        if values is None:
            return
        try:
            error = SetHouseParams(glo.path, int(values[0]), (float(values[i+1]) for i in range(5)))
            if error is not None:
                print(error)  
        except ValueError as error:
            print(error)

    elif data.startswith("request_config"):
        values: tuple[str] = parseData(data, 1)
        if values is None:
            return
        try:
            server_set_config(con, int(values[0]))
        except ValueError as error:
            print(error)
    
    elif data.startswith("accept_config"):
        values:tuple[str] = parseData(data, 1)
        if values is None:
            return
        print(f"House {values[0]} accepted configuration")

    elif data.startswith("reject_config"):
        values:tuple[str] = parseData(data, 1)
        if values is None:
            return
        print(f"House {values[0]} rejected configuration")
            
def connection_init(con:socket.socket)->None:
    global glo

    while(True):
        con.send("get_ID".encode())

        data = con.recv(1024).decode()

        if (data.startswith("request_ID")):
            pass
        elif (data.startswith("send_ID")):
            values = parseData(data, 1)
            try:
                houseID = values[0]
            except ValueError as error:
                print(error)
                return 
            if checkValidID(houseID):
                glo.addClient(con, houseID)
                thread = threading.Thread(target=handle_client, args=(con,))
                thread.start()
                break

def server_set_config(con:socket.socket, houseID: int)->bool:
    params, error = GetHouseParams(glo.path, houseID)
    if error is not None:
        print(error)
        return False
    if params is None:
        print(f"House {houseID} is not in database")
    if params.__len__() != 7:
        print("server_set_config: params != 7")
        return False

    message: str = f"""set_config HOUSEID: {params[0]},
                        TEMPMIN: {params[1]}, TEMPMAX: {params[2]}, 
                        HUMDMIN: {params[3]}, HUMDMAX: {params[4]}, 
                        MOISTMIN: {params[5]}, MOISTMAX: {params[6]}"""
    
    try:
        con.send(message.encode())
    except Exception as error:
        print(error)
        return False
        
    return True



def checkValidID(houseID: int)->bool:
    query: str = """ SELECT HOUSEID from HouseConfig WHERE HOUSEID = ?;"""
    result = DBSearch(glo.path, query, (houseID,))
    return True if result is not None else False
            



def server_handle():
    global glo
    host = '0.0.0.0'
    port = glo.port

    server_socket = socket.socket()
    try:
        server_socket.bind((host,port))
    except Exception as error:
        print(error)
        return
    
    server_socket.listen(1)

    while True:
        con, addr = server_socket.accept()
        connection_init(con)
        