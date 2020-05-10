from hero import Hero
from hist import Hist
from api import Api
from global_controller import Global_Controller
import sys

#Initialisation        
gc = Global_Controller(1280,
                       900,
                       "Lanthroff",
                       "logo32x32.png")

gc.main_screen()

try:
    f = open('edited_map.txt')
    background = 'background_edited.png'
    collision_map = f.readlines()
    for idx, i in enumerate(collision_map):
        collision_map[idx] = i.replace('\n','')
        collision_map[idx] = [h for h in collision_map[idx]]
except OSError as err:
    background = 'sprites/background.png'

try:
    f = open('char_selection.txt')
    gc.heroskin = f.read().replace('\n','')
except OSError as err:
    pass

hero_anim = {"left":{0:"sprites/"+ gc.heroskin +"/left_0.png",1:"sprites/"+ gc.heroskin +"/left_1.png",2:"sprites/"+ gc.heroskin +"/left_2.png"},
               "right":{0:"sprites/"+ gc.heroskin +"/right_0.png",1:"sprites/"+ gc.heroskin +"/right_1.png",2:"sprites/"+ gc.heroskin +"/right_2.png"},
               "up":{0:"sprites/"+ gc.heroskin +"/up_0.png",1:"sprites/"+ gc.heroskin +"/up_1.png",2:"sprites/"+ gc.heroskin +"/up_2.png"},
               "down":{0:"sprites/"+ gc.heroskin +"/down_0.png",1:"sprites/"+ gc.heroskin +"/down_1.png",2:"sprites/"+ gc.heroskin +"/down_2.png"},
               }

hero = Hero(hero_anim, 1, 1, 32, None, collision_map)

hist = Hist()
hist.bind("xpos", 35, 1000)
hist.bind("ypos", 35, 850)
hist.bind("pleasure", -100, 100)

api = Api(["turn right", "turn left", "forward", "backward", "check"])
gc.loop(60, hero, hist, api, background)   
    

