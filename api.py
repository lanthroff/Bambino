import pandas as pd
import random
from learn import Learn

#Classe contenant l'API
class Api:
    def __init__(self, cmd):
        self.cmd = cmd
        self.action = ""
        self.ready = True
        self.log = pd.DataFrame(columns = ["response", "touch_sensor"]+self.cmd)
        self.resp = 0
        self.touch_sensor = 0
        self.record = False
        self.last_actions = []
        self.status = "discovering"
        self.count = 0
        
    def compare(self, elem, li):
        res = []
        for i in li:
            res.append(int(i==elem))
        return res
    
    def work(self):
        
        if self.record:
                self.log.loc[len(self.log)] = [self.resp] \
                                              + [self.touch_sensor] \
                                              + self.compare(self.action, self.cmd)
                self.action = ""
                self.resp = 0
                self.touch_sensor = 0
                self.record = False
                
        if self.ready:
            self.count += 1
            print("action n°"+str(len(self.log)))
            self.record = True
            if len(self.log) < 1000:
                self.action = random.choice(self.cmd)
            else:
                self.status = "Baby steps"
                Learn.decision(self)
                
        if len(self.log) % 100 == 0:
            self.log.to_csv('log.csv')
