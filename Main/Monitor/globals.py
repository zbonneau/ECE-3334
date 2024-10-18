import socket
import threading
TEMP_MIN_ABS = 0
TEMP_MAX_ABS = 100
HUMD_MIN_ABS = 0
HUMD_MAX_ABS = 100
MOIST_MIN_ABS = 0
MOIST_MAX_ABS = 100
DBPATH = "Main\\Monitor\\test.db"
PORT = 5000




class globals:
    def __init__(self):
        self.clients: dict[int:(socket.socket)] = {}
        self.path:str = DBPATH
        self.port:int = PORT

    def addClient(self, con:socket.socket, houseID: int)->None:
        if con is not None:
            self.dropClient(houseID)
            self.clients[houseID] = con
            
    def dropClient(self, houseID: int)->None:
        if (self.clients[houseID] is None):
            return
        try:
            client:socket.socket = self.clients[houseID]
            client.close() 
        except AttributeError:
            pass
        except OSError:
            pass
        finally:
            del self.clients[houseID]
        
        

glo:globals = globals()

