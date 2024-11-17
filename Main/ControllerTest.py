from socket import socket, SHUT_RDWR
from threading import Thread
import sqlite3 as sql

def Listen(con:socket, addr)->None:
    try:
        while True:
            data = con.recv(1024).decode()
            if not data:
                con.shutdown(SHUT_RDWR)
                con.close()
                return
            for line in data.splitlines():
                print(f"\nclient @{addr[0]}:{addr[1]} >{line}\nserver >", end='')
    
    except Exception as error:
        print(error)

def respond(con:socket)->None:
    try:
        while con:
            #print("server >", end = '', flush=True)
            message = input()
            if (message == 'q'):
                break
            if con:
                con.send(message.encode())
        
    except Exception as error:
        print(error)

if __name__ == "__main__":
    server = socket()
    server.bind(('0.0.0.0', 5000))

    # con = sql.Connection("Controller\\test.db")
    # con.execute("""
    #         CREATE TABLE IF NOT EXISTS data(
    #         TIMESTAMP TEXT,
    #         HOUSEID   INTEGER,                          
    #         TEMP      REAL,
    #         HUMIDITY  REAL,
    #         MOISTURE  REAL
    #         );
    #         """ )
    # paramss = [
    #     ('2024-10-10 10:00', 1, 10, 20, 20),
    #     ('2024-10-10 10:15', 1, 11, 21, 22),
    #     ('2024-10-10 10:30', 1, 12, 22, 23),
    #     ('2024-10-10 10:45', 1, 13, 23, 24),
    #     ('2024-10-10 11:00', 1, 14, 24, 25),
    #     ('2024-10-10 10:15', 1, 15, 25, 26)
    # ]
    # for params in paramss:
    #     con.execute("INSERT INTO data VALUES(?,?,?,?,?);", params)
    # con.commit()
    # con.close()

    server.settimeout(10)
    try:
        while True:
            try:
                server.listen(1)
                con,addr = server.accept()
            
            except TimeoutError:
                continue

            print(f'Connected pi@{addr[0]}')

            task = Thread(target=Listen, args=(con,addr))
            task.start()

            respond(con)
            task.join()


    except KeyboardInterrupt:
        try:
            con.shutdown(SHUT_RDWR)
            con.close()
        except Exception:
            pass