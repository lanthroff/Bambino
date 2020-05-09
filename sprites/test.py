import cv2
import numpy as np

img = cv2.imread('background.png')


print(img[0:32,0:32, :].shape)


