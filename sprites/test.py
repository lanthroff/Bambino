import cv2
import numpy as np

img = cv2.imread('background.png')

for i in img:
    for j in i:
        if not j[0] == 0:
            print(j)
            break


