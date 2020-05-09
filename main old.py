import pygame
import time
import cv2
import numpy

#Classe de controle global pour l'affichage et les inputs
class Global_Controller:
    def __init__(self,
                 screen_width,
                 screen_height,
                 title,
                 logo,
                 background='black',
                 
                 ):
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        pygame.display.set_caption(title)
        self.logo = pygame.image.load(logo)
        pygame.display.set_icon(self.logo)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        if background == 'black':
            self.background = (0,0,0)
        else:
            pass
        self.obj = []

    def loop(self, fps, hero):
        deltax = deltay = 0
        t0 = time.time()
        
        while True:
            
            self.screen.fill(self.background)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN and hero.move == 0:
                    if event.key == pygame.K_LEFT:
                        if hero.direction == "left":
                            deltax = -1
                            deltay = 0
                            hero.move = 25
                            hero.stance = 1
                            
                        hero.image = hero.left[0]
                        hero.direction = "left"
                        
                    if event.key == pygame.K_RIGHT:
                        if hero.direction == "right":
                            deltax = 1
                            deltay = 0
                            hero.move = 25
                            hero.stance = 1
                            
                        hero.image = hero.right[0]
                        hero.direction = "right"
                        
                    if event.key == pygame.K_UP:
                        if hero.direction == "up":
                            deltay = -1
                            deltax = 0
                            hero.move = 25
                            hero.stance = 1
                            
                        hero.image = hero.up[0]
                        hero.direction = "up"
                        
                    if event.key == pygame.K_DOWN:
                        if hero.direction == "down":
                            deltay = 1
                            deltax = 0
                            hero.move = 25
                            hero.stance = 1
                            
                        hero.image = hero.down[0]
                        hero.direction = "down"
                        
            if hero.move > 0:
                dt = time.time() - t0
                time.sleep(1/fps - dt)
                hero.xpos += deltax 
                hero.ypos += deltay 
                hero.move -= 1
                if hero.move % 7 == 0:
                    hero.stance += 1
                if hero.stance == 3:
                    hero.stance = 0
                hero.image = getattr(hero, hero.direction)[hero.stance]
                
            elif hero.move == 0:
                hero.image = getattr(hero, hero.direction)[0]
            self.screen.blit(hero.image, (hero.xpos, hero.ypos))
            pygame.display.flip()
            t0 = time.time()

    def update_item(self, item):
        self.obj.append(item)
                
#Classe contenant les differents objets de la scene            
class Hero:
    def __init__(self,
                 anim,
                 xpos,
                 ypos,
                 transparent,
                 movable):

        self.direction = "right"
        self.image = pygame.image.load(anim["right"][0])
        for side in anim:
            setattr(self, side, [pygame.image.load(anim[side][i]) for i in range(3)])
        self.xpos = xpos
        self.ypos = ypos
        self.move = 0
        self.stance = 0
        if transparent == "white":
            self.image.set_colorkey((255, 255, 255))


#Initialisation        
gc = Global_Controller(800,
                       600,
                       "Lanthroff",
                       "logo32x32.png")

hero_anim = {"left":{0:"sprites/left_0.png",1:"sprites/left_1.png",2:"sprites/left_2.png"},
               "right":{0:"sprites/right_0.png",1:"sprites/right_1.png",2:"sprites/right_2.png"},
               "up":{0:"sprites/up_0.png",1:"sprites/up_1.png",2:"sprites/up_2.png"},
               "down":{0:"sprites/down_0.png",1:"sprites/down_1.png",2:"sprites/down_2.png"},
               }

char = Hero(hero_anim, 50, 50, None, True)

gc.update_item(char)
gc.loop(60, char)


    

