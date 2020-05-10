import cv2
import numpy as np
import os


position = ["down",
            "left",
            "right",
            "up"]

state = {0:1,
         1:0,
         2:2}


directories = os.listdir(dir)

for d in directories:
    if d.find(".") == -1:
        img = cv2.imread(d+'/hero.png')
        for i in range(len(position)):
            for j in range(3):
                cv2.imwrite(d+"/"+position[i]+"_"+str(state[j])+".png", img[i*32:(i+1)*32,j*32:(j+1)*32])
        
