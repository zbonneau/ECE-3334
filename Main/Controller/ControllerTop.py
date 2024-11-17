from threading import Thread
from greenhouse_main import main as greenhouseMain
from ControllerComms import clientThread
from globals import glo



def startup()->None:
    comms: Thread = Thread(target=clientThread)
    main: Thread  = Thread(target=greenhouseMain)

    comms.start()
    main.start()
    try:
        while not glo.closeApplication:
            continue
    except KeyboardInterrupt:
        print("User-Event for Shutdown")
    except Exception as error:
        print(f"Top: {error.__str__()}")

    finally:
        glo.closeApplication = True # Tell threads to close. may take Up to "PollInterval" minutes to execute 
        main.join()
        comms.join()


if __name__ == "__main__":
    startup()
    glo.closeSocket()