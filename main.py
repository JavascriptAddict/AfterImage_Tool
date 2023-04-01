from intercept import Intercepter
from proxy import *
import config
import threading
import time
import server

PROXIESLOCK = threading.Lock()

def manageProxies():
    '''Thread function to update proxies list every few mins'''
    while True:
        PROXIESLOCK.acquire()
        config.PROXIES.update()
        PROXIESLOCK.release()
        # Update proxy list every 15 mins
        time.sleep(900)

def main():
    '''Main function'''
    listenerThread = threading.Thread(target=Intercepter)
    proxiesThread = threading.Thread(target=manageProxies)
    serverThread = threading.Thread(target=server.app.run, kwargs={"debug":True, "use_reloader":False})
    listenerThread.daemon = True
    proxiesThread.daemon = True
    serverThread.daemon = True
    serverThread.start()
    proxiesThread.start()
    listenerThread.start()
    # Keep main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()