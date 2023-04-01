import config

def getAwaitDictByKey(key):
    return [element for element in config.ATTACKSAWAIT["attacks"] if element["uid"] == key]

def getAwaitIndexByKey(key):
    count = 0
    while count < len(config.ATTACKSAWAIT["attacks"]):
        if config.ATTACKSAWAIT["attacks"][count]["uid"] == key:
            return count