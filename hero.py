import pygame
import cv2
           
class Hero:
    def __init__(self,
                 anim,
                 ipos,
                 jpos,
                 dist,
                 transparent,
                 collider):

        self.direction = 0
        self.image = pygame.image.load(anim["right"][0])
        for side in anim:
            setattr(self, side, [pygame.image.load(anim[side][i]) for i in range(3)])
        self.ipos = ipos
        self.jpos = jpos
        self.xpos = jpos*32
        self.ypos = ipos*32
        self.move = 0
        self.dist = dist
        self.stance = 0
        self.rotation = ["right", "down", "left", "up"]
        self.collider = collider
        self.reverto = {False:{"right":"right",
                               "left":"left",
                               "up":"up",
                               "down":"down"},
                        True:{"right":"left",
                              "left":"right",
                              "up":"down",
                              "down":"up"}
                        }

        self.pleasure = 0
        self.interaction = {"forward":2,
                            "backward":-1,
                            "wall":-10,
                            "turn":-1,
                            "check":-1}
        
        #Transparent option
        if transparent == "white":
            self.image.set_colorkey((255, 255, 255))
        if transparent == "black":
            self.image.set_colorkey((0, 0, 0))
        
    def collide(self, reverse):
        if self.reverto[reverse][self.rotation[self.direction]] == "right":
            return self.collider[self.ipos][self.jpos+1] == 'X'
                        
        elif self.reverto[reverse][self.rotation[self.direction]] == "left":
            return self.collider[self.ipos][self.jpos-1] == 'X'
      
        elif self.reverto[reverse][self.rotation[self.direction]] == "down":
            return self.collider[self.ipos+1][self.jpos] == 'X'
        
        elif self.reverto[reverse][self.rotation[self.direction]] == "up":
            return self.collider[self.ipos-1][self.jpos] == 'X'
                

