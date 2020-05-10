import pygame
import time
from editor import Editor
from selection import Selection

class Global_Controller:
    def __init__(self,
                 screen_width,
                 screen_height,
                 title,
                 logo
                 ):

        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        pygame.display.set_caption(title)
        self.logo = pygame.image.load(logo)
        pygame.display.set_icon(self.logo)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.obj = []
        self.heroskin = "bambino_17"

    def main_screen(self):
        done = True
        color_1 = (255,255,0)
        color_2 = (0,255,0)
        while done:
            pygame.draw.rect(self.screen, (0,0,0),(0,0,1280,900))
            editor = start = hero_sel = False
            start_color = editor_color = hero_color = color_1
            b1_color = b2_color = b3_color = color_2
            x, y = pygame.mouse.get_pos()
            if x > 450 and x < 750:
                if y > 200 and y < 300:
                    b1_color = color_1
                    editor_color = color_2
                    editor = True
                if y > 400 and y < 500:
                    b2_color = color_1
                    start_color = color_2
                    start = True
                if y > 600 and y < 700:
                    b3_color = color_1
                    hero_color = color_2
                    hero_sel = True
            
                
            pygame.draw.rect(self.screen, b1_color,(450,200,300,100))
            pygame.draw.rect(self.screen, b2_color,(450,400,300,100))
            pygame.draw.rect(self.screen, b3_color,(450,600,300,100))

            #Event handler
            for event in pygame.event.get():
                        
                #Mouse Click event
                if event.type == pygame.MOUSEBUTTONUP:
                    if editor:
                        Editor.start(self)
                    if start:
                        done = False
                    if hero_sel:
                        Selection.start(self)
                        
                #Escape condition        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = False
            #Map editor text
            font = pygame.font.SysFont("comicsansms", 40)
            text = font.render("Map Editor", False, editor_color)
            self.screen.blit(text,(600 - text.get_width() // 2,
                                   250 - text.get_height() // 2))
            #Start
            font = pygame.font.SysFont("comicsansms", 40)
            text = font.render("Start", False, start_color)
            self.screen.blit(text,(600 - text.get_width() // 2,
                                   450 - text.get_height() // 2))

            #Start
            font = pygame.font.SysFont("comicsansms", 40)
            text = font.render("Hero Selection", False, hero_color)
            self.screen.blit(text,(600 - text.get_width() // 2,
                                   650 - text.get_height() // 2))
            
            #Show
            pygame.display.flip()
            
    def loop(self, fps, hero, hist, api, background):
        self.background = pygame.image.load(background)
        deltax = deltay = 0
        t0 = time.time()
        done = True
        
        while done:
            
            #Escape condition
            for event in pygame.event.get():
                                   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = False
                                
            self.screen.blit(self.background, (0, 0))
            # Api actions
            if not api.action == "":
                api.ready = False
                if hero.move == 0:

                    if api.action == "check":
                        deltax = deltay = 0
                        hero.pleasure += hero.interaction["check"]
                        api.resp = hero.interaction["check"]

                        if hero.collide(False):
                            api.touch_sensor = 1
                        else:
                            api.touch_sensor = -1
                            
                    elif api.action == "turn left":
                        
                        deltax = deltay = 0
                        hero.pleasure += hero.interaction["turn"]
                        api.resp = hero.interaction["turn"]
                        hero.direction -= 1
                        if hero.direction < 0:
                            hero.direction = 3

                        hero.image = getattr(hero, hero.rotation[hero.direction])[0]
                        
                    elif api.action == "turn right":

                        deltax = deltay = 0
                        hero.pleasure += hero.interaction["turn"]
                        api.resp = hero.interaction["turn"]
                        hero.direction += 1
                        if hero.direction > 3:
                            hero.direction = 0

                        hero.image = getattr(hero, hero.rotation[hero.direction])[0]
                        
                    elif api.action == "forward":

                        if hero.rotation[hero.direction] == "right":
                            if not hero.collide(False):
                                
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                deltax = 1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "down":
                            if not hero.collide(False):
                                
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                deltax = 0
                                deltay = 1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "left":
                            if not hero.collide(False):
                                
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                deltax = -1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "up":
                            if not hero.collide(False):
                                
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                deltax = 0
                                deltay = -1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                            
                    elif api.action == "backward":
    
                        if hero.rotation[hero.direction] == "right":
                            if not hero.collide(True):
                                
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                deltax = -1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "down":
                            if not hero.collide(True):
                                
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                deltax = 0
                                deltay = -1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "left":
                            if not hero.collide(True):
                                
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                deltax = 1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                    
                        elif hero.rotation[hero.direction] == "up":
                            if not hero.collide(True):
                                
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                deltax = 0
                                deltay = 1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                deltax = 0
                                deltay = 0
                                
            if hero.pleasure < -100:
                hero.pleasure = -100
            elif hero.pleasure > 100:
                hero.pleasure = 100
                                    
            if hero.move > 0:
                dt = time.time() - t0
                wait = 1/fps - dt
                if wait > 0:
                    time.sleep(wait)
                hero.xpos += deltax 
                hero.ypos += deltay 
                hero.move -= 1
                if hero.move % 7 == 0:
                    hero.stance += 1
                if hero.stance == 3:
                    hero.stance = 0
                hero.image = getattr(hero, hero.rotation[hero.direction])[hero.stance]
    
            elif hero.move == 0 and not api.ready:
                #Update ipos and jpos
                hero.ipos += deltay
                hero.jpos += deltax
                            
                #Set hero to neutral position
                hero.image = getattr(hero, hero.rotation[hero.direction])[0]

                #Reset Api
                api.ready = True
                
            #Use the api
            api.work()

            #Api update status
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(api.status, False, (0, 255, 0))
            self.screen.blit(text,(1150 - text.get_width() // 2,
                                   600 - text.get_height() // 2))

            #Update count
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render("Count : {}".format(api.count), False, (0, 0, 255))
            self.screen.blit(text,(1150 - text.get_width() // 2,
                                   650 - text.get_height() // 2))
            #Hist bar for stats
            hist.update(hero)
            for h in hist.rect: 
                pygame.draw.rect(self.screen,(h[0],h[1],h[2]),(h[3],h[4],h[5],h[6]))
            for t in hist.text:
                font = pygame.font.SysFont(t[0], t[1])
                text = font.render(t[2], t[3], t[4])
                self.screen.blit(text,(
                                 t[5] - text.get_width() // 2,
                                 t[6] - text.get_height() // 2))
                
            self.screen.blit(hero.image, (hero.xpos, hero.ypos))
            pygame.display.flip()
            t0 = time.time()
        pygame.quit()
