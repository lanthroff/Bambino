import cv2
import numpy as np
import random

image = [[(0,0,0) for _ in range(1280)] for _ in range(900)]
image = np.array(image).astype('uint8')

f = open("gen_32.txt", "r")

data = f.readlines()
for idx, i in enumerate(data):
    data[idx] = i.replace('\n','')
    data[idx] = [h for h in data[idx]]

def grid(data, c):
    for idx, i in enumerate(data):
        for jdx, j in enumerate(i):
            if idx > c and idx < 900-c and jdx > c and jdx < 1000-c:
                if idx % c == 0:
                    data[idx][jdx][0] = 255
                    data[idx][jdx][1] = 255
                    data[idx][jdx][2] = 255
                if jdx % c == 0:
                    data[idx][jdx][0] = 255
                    data[idx][jdx][1] = 255
                    data[idx][jdx][2] = 255
    return data

def wall(row, col, image, c):
    for i in range(row*c, (row+1)*c):
        for j in range(col*c, (col+1)*c):
            image[i][j][0] = 255
    return image

def valid_hole(t, holes, lim):
    for h in holes:
        if abs(holes[h] - t) < lim:
            return False
    return True

def random_line(data):
    line = random.randint(5, 85)
    data[line] = data[line] = ['X' for _ in range(len(data[line]))]
    #Random hole
    n_hole = random.randint(1,3)
    holes = {}
    for i in range(n_hole):
        tmp = random.randint(1,99)
        while not valid_hole(tmp, holes, 15):
            tmp = random.randint(1,99)
        holes[i] = tmp
    for i in holes:
        data[line][holes[i]] = ' '
        if holes[i] > 1:
            data[line][holes[i]-1] = ' '
        else:
            data[line][holes[i]+2] = ' '
        if holes[i] < 99:
            data[line][holes[i]+1] = ' '
        else:
            data[line][holes[i]-2] = ' '
    return data

#Generer lab
#data = random_line(data)
block_size = 32
image = grid(image, block_size)
for idr, row in enumerate(data):   
    for idc, col in enumerate(row):
        if data[idr][idc] == 'X':
            image = wall(idr, idc, image, block_size)

cv2.imshow('test', image)
cv2.waitKey(0)
