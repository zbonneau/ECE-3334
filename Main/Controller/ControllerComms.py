from globals import glo, PORT, HOUSEPARAMS, POLLINTERVAL, MAXATTEMPTS
from globals import DEBUGCOMMS as DEBUG
from socket import socket
from DBFunc import DBInsert, DBSearch, parseData
from datetime import datetime, timedelta


def handleData(data:str)->bool: # returns true if loop should break
    if data.startswith('set_config'):
        params = parseData(data, HOUSEPARAMS)
        passed:bool = True
        ## Check format
        try:
            formatted = (int(params[0]), 
                         float(params[1]),
                         float(params[2]),
                         float(params[3]),
                         float(params[4]),
                         float(params[5]),
                         float(params[6]),
                         params[7],
                         )
            ## Check if houseID Correct
            if (glo.houseID != formatted[0]):
                passed = False
                if DEBUG:
                    print("set_config Error: wrong HOUSEID")
            
            ## Check for vaguely adequete parameters
            if (formatted[1] < 0 or formatted[2] > 40 or formatted[1] > formatted[2]):
                passed = False
                if DEBUG:
                    print(f"set_config failed: BAD TEMP >({formatted[1], formatted[2]})")
            
            if (formatted[3] < 0 or formatted[4] > 100 or formatted[3] > formatted[4]):
                passed = False
                if DEBUG:
                    print(f"set_config failed: BAD HUMD >({formatted[3], formatted[4]})")
            
            if (formatted[5] < 0 or formatted[6] > 100 or formatted[5] > formatted[6]):
                passed = False
                if DEBUG:
                    print(f"set_config failed: BAD MOIST >({formatted[5], formatted[6]})")
            
            if (formatted[7] < glo.timeStamp):
                passed = False
                if DEBUG:
                    print(f"set-config failed: OLD TIMESTAMP >({formatted[7]}, {glo.timeStamp})")

            if passed:
                # Update house params if passed
                glo.editConfig(formatted)
            
        except Exception as error:
            print(f"set_config parse error: {error}")
            
        
        send_config()
        return False

    elif data.startswith('get_data'):
        # Check parse
        params = parseData(data, 2)
        try:
            houseID = int(params[0])
            timeStamp = params[1]
        except Exception as error:
            if (DEBUG):
                print(f"get_data parse error: {error}")
            send_config()
            return False
        
        if (houseID != glo.houseID):
            if (DEBUG):
                print(f"get_data failed: wrong houseID")
            send_config()
            return False
        message = "SELECT * FROM data WHERE TIMESTAMP > ? ORDER BY TIMESTAMP;"

        data:tuple = DBSearch(glo.path, message, (timeStamp,))
        ## IF DB Empty, break connection
        if (data is None or data.__len__() == 0):
            return True # if no data in this bunch, don't delete the rest
        
        for entry in data:
            send_data(entry)

        # Delete from table all entries that the monitor claims to have (ie. cumulative ack)
        message = "DELETE FROM data WHERE TIMESTAMP <= ?;"
        DBInsert(glo.path, message, (timeStamp,))
        return True

    else:
        if DEBUG:
            print(f"PARSE ERROR: >{data[0:19]}")
        return True

def send_data(data:tuple)->None:
    if not data or data.__len__() != 5:
        return
    try:
        message = f"send_data HOUSEID: {data[1]}, "
        message+= f"TIMESTAMP: {data[0]}, "
        message+= f"TEMP: {data[2]}, "
        message+= f"HUMD: {data[3]}, "
        message+= f"MOIST: {data[4]}\n"
        
        if DEBUG:
            print(f"pi >{message}")

        glo.socket.send(message.encode())

    except Exception as error:
        if DEBUG:
            print(f"send_data() Error: {error}")
    
    
def send_config()->None:
    message = f"send_config HOUSEID: {glo.houseID}, TEMPMIN: {glo.tempMin}, TEMPMAX: {glo.tempMax}, "  
    message+= f"HUMDMIN: {glo.humdMin}, HUMDMAX: {glo.humdMax}, "
    message+= f"MOISTMIN: {glo.moistMin}, MOISTMAX: {glo.moistMax}, "
    message+= f"TIMESTAMP: {glo.timeStamp}\n"

    if DEBUG:
        print(f"pi >{message}")
    if glo.socket:
        glo.socket.send(message.encode())

def clientHandle()->None:
    glo.socket = socket()
    glo.socket.settimeout(20)
    #glo.socket.settimeout(10) # Timeout exception after 10 seconds
    attempts = 0

    # Connect socket to server
    while True:
        try:
            attempts += 1
            glo.socket.connect((glo.IP,PORT))
            if DEBUG:
                print(f"Socket connected to {glo.IP}:{PORT}")
            break
        except Exception as error:
            glo.closeSocket()
            return
    
    # Run Init
    send_config()

    while True:
        try:
            data = glo.socket.recv(1024).decode()
        except Exception as error:
            print(f"Listen error: {error}")
            break

        if DEBUG:
            print(f"server@{glo.IP} >{data}")

        if not data or handleData(data):
            break
    
    glo.closeSocket()

def clientThread()->None:
    from time import sleep

    # Generate poll every POLLINTERVAL minutes
    interval = timedelta(minutes = POLLINTERVAL)
    while not glo.closeApplication:
        now = datetime.now()
        nextPoll = now.replace(minute= (now.minute//POLLINTERVAL) * POLLINTERVAL, second = 0, microsecond=0)
        nextPoll += interval        
        print(f"Next Poll @ {nextPoll.isoformat(sep=' ', timespec= 'minutes')}")
        
        sleep((nextPoll-now).total_seconds())
        if glo.closeApplication:
            break # Check after long sleep
        
        # fetch current signals, place in local DB
        try:
            params = (nextPoll.isoformat(sep=' ', timespec='minutes'),
                    int(glo.houseID),
                    float(glo.realTemp),
                    float(glo.realHumd),
                    float(glo.realMoist))
            command = "INSERT INTO data VALUES(?,?,?,?,?);"
            DBInsert(glo.path, command, params)
        except Exception:
            # Generic Exception Handler. Does nothing with exception, just prevents program exit
            pass

        finally:
            clientHandle()
  
    
if __name__ == "__main__":
    try:
        while True:
            input("Run Client Handle (Ctrl+C to quit) >")
            clientHandle()
    
    except KeyboardInterrupt:
        print("Closing Client Handle")
        glo.closeSocket()