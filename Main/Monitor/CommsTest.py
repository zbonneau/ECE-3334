from socket import socket, SHUT_RDWR
# from globals import PORT
from threading import Thread

def listenServer(client:socket)->None:
    while 1:
        try:
            message = client.recv(1024).decode()

        except Exception as error:
            print(f"Listen Error: {error}")
            return

        if not message:
            return
        print(f"Server >{message}")

def emulateClient(client:socket)->bool:
    if not client:
        return False
    message = input("Send a message (q to quit): ")
    if message == "q":
        return False
    client.send(message.encode())
    return True


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    client = socket()
    try:
        client.connect((host, port))
    except Exception as error:
        print(f"Connect failed: {error}")
        exit(1)

    thread:Thread = Thread(target=listenServer, args=(client,))
    thread.start()

    while 1:
         if not emulateClient(client):
             break
         
    client.shutdown(SHUT_RDWR)
    thread.join()
    client.close()



    