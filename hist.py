#Classe contenant les differentes valeurs à visualiser            
class Hist:
    def __init__(self):
        self.item = []
        self.settings = {}
        self.rect = []
        self.text = []
        
    def bind(self, b, mini, maxi):
        d = len(self.item)
        self.item.append(b)
        self.settings[b] = [0, mini, maxi]
        self.rect.append([0, 255, 0, 1020, 35+(d*50), 255, 20])
        self.text.append(["comicsansms",
                          20,
                          b,
                          False,
                          (255, 0, 0),
                          1150,
                          20+(d*50)])

    def update(self, hero):
        for idx, i in enumerate(self.item):
            self.settings[i][0] = getattr(hero, i)
            pct = (self.settings[i][0] - self.settings[i][1]) / (self.settings[i][2] - self.settings[i][1])
            self.rect[idx][5] = int(255*pct)
