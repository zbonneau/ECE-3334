from threading import Thread
from greenhouse_main import main
from ControllerComms import clientThread
from globals import glo



def startup()->None:
    comms: Thread = Thread(target=clientThread)
    main: Thread  = Thread(target=main)

    comms.start()
    main.start()
    try:
        while True:
            pass
    except Exception:
        comms.join()
        main.join()


if __name__ == "__main__":
    startup()
    glo.closeSocket()