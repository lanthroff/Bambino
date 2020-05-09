from hero import Hero
from hist import Hist
from api import Api
from global_controller import Global_Controller

#Initialisation        
gc = Global_Controller(1280,
                       900,
                       "Lanthroff",
                       "logo32x32.png",
                       "sprites/background.png")

hero_anim = {"left":{0:"sprites/left_0.png",1:"sprites/left_1.png",2:"sprites/left_2.png"},
               "right":{0:"sprites/right_0.png",1:"sprites/right_1.png",2:"sprites/right_2.png"},
               "up":{0:"sprites/up_0.png",1:"sprites/up_1.png",2:"sprites/up_2.png"},
               "down":{0:"sprites/down_0.png",1:"sprites/down_1.png",2:"sprites/down_2.png"},
               }

hero = Hero(hero_anim, 180, 450, 25, None, 'sprites/background.png')

hist = Hist()
hist.bind("xpos", 35, 1000)
hist.bind("ypos", 35, 850)
hist.bind("pleasure", -100, 100)

api = Api(["turn right", "turn left", "forward", "backward", "check"])
gc.loop(60, hero, hist, api)   
    

