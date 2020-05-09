import pygame
import time

class Global_Controller:
    def __init__(self,
                 screen_width,
                 screen_height,
                 title,
                 logo,
                 background
                 ):

        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        pygame.display.set_caption(title)
        self.logo = pygame.image.load(logo)
        pygame.display.set_icon(self.logo)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load(background)
        self.obj = []


    def loop(self, fps, hero, hist, api):
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

                        hero.pleasure += hero.interaction["check"]
                        api.resp = hero.interaction["check"]

                        if hero.collide(False):
                            api.touch_sensor = 1
                        else:
                            api.touch_sensor = -1
                            
                    elif api.action == "turn left":

                        hero.pleasure += hero.interaction["turn"]
                        api.resp = hero.interaction["turn"]
                        hero.direction -= 1
                        if hero.direction < 0:
                            hero.direction = 3

                        hero.image = getattr(hero, hero.rotation[hero.direction])[0]
                        
                    elif api.action == "turn right":

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
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "down":
                            if not hero.collide(False):
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 0
                                deltay = 1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "left":
                            if not hero.collide(False):
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = -1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "up":
                            if not hero.collide(False):
                                hero.pleasure += hero.interaction["forward"]
                                api.resp = hero.interaction["forward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 0
                                deltay = -1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                            
                    elif api.action == "backward":
                        api.action = ""
                        if hero.rotation[hero.direction] == "right":
                            if not hero.collide(True):
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = -1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "down":
                            if not hero.collide(True):
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 0
                                deltay = -1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "left":
                            if not hero.collide(True):
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 1
                                deltay = 0
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                                    
                        elif hero.rotation[hero.direction] == "up":
                            if not hero.collide(True):
                                hero.pleasure += hero.interaction["backward"]
                                api.resp = hero.interaction["backward"]
                                if hero.pleasure > 100:
                                    hero.pleasure = 100
                                deltax = 0
                                deltay = 1
                                hero.move = hero.dist
                                hero.stance = 1
                            else:
                                hero.pleasure += hero.interaction["wall"]
                                api.resp = hero.interaction["wall"]
                                if hero.pleasure < -100:
                                    hero.pleasure = -100
                 
                        
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
                
            elif hero.move == 0:
                hero.image = getattr(hero, hero.rotation[hero.direction])[0]
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
