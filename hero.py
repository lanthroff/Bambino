import pygame
import cv2
           
class Hero:
    def __init__(self,
                 anim,
                 xpos,
                 ypos,
                 dist,
                 transparent,
                 collider):

        self.direction = 0
        self.image = pygame.image.load(anim["right"][0])
        for side in anim:
            setattr(self, side, [pygame.image.load(anim[side][i]) for i in range(3)])
        self.xpos = xpos
        self.ypos = ypos
        self.dist = dist
        self.move = 0
        self.stance = 0
        self.rotation = ["right", "down", "left", "up"]
        self.collider = cv2.imread(collider)
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
        
    def collide(self, reverse):
        if self.reverto[reverse][self.rotation[self.direction]] == "right":
            for x in range(self.xpos+32, self.xpos+self.dist+32):
                if self.collider[self.ypos][x][0] == 255:
                    return True
                if self.collider[self.ypos+32][x][0] == 255:
                    return True
                
        elif self.reverto[reverse][self.rotation[self.direction]] == "left":
            for x in range(self.xpos, self.xpos-self.dist, -1):
                if self.collider[self.ypos][x][0] == 255:
                    return True
                if self.collider[self.ypos+32][x][0] == 255:
                    return True
                
        elif self.reverto[reverse][self.rotation[self.direction]] == "down":
            for y in range(self.ypos+32, self.ypos+self.dist+32):
                if self.collider[y][self.xpos][0] == 255:
                    return True
                if self.collider[y][self.xpos+32][0] == 255:
                    return True
                
        elif self.reverto[reverse][self.rotation[self.direction]] == "up":
            for y in range(self.ypos, self.ypos-self.dist, -1):
                if self.collider[y][self.xpos][0] == 255:
                    return True
                if self.collider[y][self.xpos+32][0] == 255:
                    return True

        return False
