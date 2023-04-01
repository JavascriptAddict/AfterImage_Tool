from datetime import datetime

class Logger:
    def __init__(self):
        pass
    def out(self, message):
        now = datetime.now()
        print("[{}] => {}".format(now.strftime("%m/%d/%Y, %H:%M:%S"), message))
    
    def traffic(self, src, dest):
        now = datetime.now()
        print("[{}] {} <=> {}".format(now.strftime("%m/%d/%Y, %H:%M:%S"), src, dest))