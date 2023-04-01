import socket 
import config
import utils
import threading        
import uuid   
from log import Logger

ATTACKLOCK = threading.Lock()

class Intercepter:
    '''Intercepter class'''
    def __init__(self):
        '''Init function'''
        self.logger = Logger()
        self.state = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.out("Receiver socket successfully created")
        self.port = 12345               
        self.sock.bind(('127.0.0.1', self.port))        
        self.logger.out("Socket binded to %s" %(self.port))
        self.sock.listen()    
        self.logger.out("Socket is listening")  
        self.retryCount = 0
        self.respState = False
        self.response = None

        while self.state:
            conn, addr = self.sock.accept()    
            self.logger.traffic(str(addr), "AfterImage")
            data = conn.recv(1024)
            if not data:
                conn.close()
                continue
            newThread = threading.Thread(target=self.awaitAttackDetails, args=(str(addr), conn, data))            
            newThread.start()

    def awaitAttackDetails(self, srcAddr, conn, data):
        # Need think how specify target IP to proxy server
        newUID = uuid.uuid4().hex
        srcAddr = eval(srcAddr)
        # Src IP, Update State, Target IP
        config.ATTACKSAWAIT["attacks"].append({"uid": newUID, "srcaddr": srcAddr[0], "srcport": srcAddr[1], "attack": False, "dstaddr": "0.0.0.0"})
        while True:
            element = utils.getAwaitDictByKey(newUID)
            if element[0]["attack"] is True:
                ATTACKLOCK.acquire()
                config.ATTACKS["attacks"].append(element[0])
                print([d for d in config.ATTACKSAWAIT["attacks"] if d.get('uid') != newUID])
                config.ATTACKSAWAIT["attacks"] = [d for d in config.ATTACKSAWAIT["attacks"] if d.get('uid') != newUID]
                ATTACKLOCK.release()
                break
        self.transmit(data)
        conn.sendall(self.response)
        conn.close()


    def transmit(self, data):
        respState = False
        while respState is False and self.retryCount < 6:
            try:
                proxy = config.PROXIES.getProxy()
                newClient = socket.socket()
                self.logger.traffic("AfterImage", proxy.ip)  
                newClient.connect((proxy.ip, int(proxy.port)))
                if type(data) is str:
                    data = data.encode('utf-8')
                newClient.send(data)
                self.response = newClient.recv(1024)
                newClient.close()
                respState  = True
            except socket.error as e:
                self.logger.out("Proxy Connection Fail: {}:{}".format(proxy.ip, proxy.port))
                config.PROXIES.updateProxyConn(proxy)
                if self.retryCount < 5:
                    self.retryCount += 1
                    self.logger.out("Retrying: Count {}".format(self.retryCount))
                    continue
                self.response = "Failed to execute attack via after {} times".format(self.retryCount).encode("utf-8")
                self.logger.out(self.response)
                respState  = False
                break
        self.retryCount = 0



