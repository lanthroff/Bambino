import pygame
import numpy as np
import cv2
import time
import sys

class Editor:
    def wall(row, col, image, c, color):

        image[row:row+c, col:col+c, :] = color
        return image

    def data2image(data, img, block_size, grid):
        black_square = np.array([[(0,0,0) for _ in range(32)] for _ in range(32)]).astype("uint8")
        blue_square = np.array([[(255,0,0) for _ in range(32)] for _ in range(32)]).astype("uint8")

        for idr, row in enumerate(data):   
            for idc, col in enumerate(row):
                if data[idr][idc] == 'X':
                    img = Editor.wall(idr*block_size, idc*block_size, img, block_size, blue_square)
            
                elif data[idr][idc] == 'E':
                    img = Editor.wall(idr*block_size, idc*block_size, img, block_size, black_square)
                    data[idr][idc] = ' '
        if grid:
            img = Editor.grid(img, 32, data)            
        cv2.imwrite('background_edited.png', img)  

    def grid(img, c, data):
        for idx, i in enumerate(img):
            for jdx, j in enumerate(i):
                if idx > c and idx < (len(data)-1)*c and jdx > c and jdx < (len(data[0])-1)*c:
                    if idx % c == 0:
                        img[idx][jdx][0] = 255
                        img[idx][jdx][1] = 255
                        img[idx][jdx][2] = 255
                    if jdx % c == 0:
                        img[idx][jdx][0] = 255
                        img[idx][jdx][1] = 255
                        img[idx][jdx][2] = 255
        return img

    def start(gc):
        #clear screen
        pygame.draw.rect(gc.screen, (0,0,0),(0,0,1280,900))
        pygame.display.flip()

        image = [[(0,0,0) for _ in range(1280)] for _ in range(900)]
        image = np.array(image).astype('uint8')

        try:
            f = open('edited_map.txt')
        except OSError as err:
            f = open("default_map.txt", "r")
        data = f.readlines()
        for idx, i in enumerate(data):
            data[idx] = i.replace('\n','')
            data[idx] = [h for h in data[idx]]

        #Setup UI variables
        buttons = {}
        buttons['Add Block'] = {'status' : True,
                                'fontfamily': 'comicsansms',
                                'fontsize': 25,
                                'color off':(255,255,0),
                                'color on': (0,255,0),
                                'color' : (0,255,0),
                                'over' : (105,105,105),
                                'overed': False,
                                'position': (1150,50)}

        buttons['Remove Block'] = {'status' : False,
                                'fontfamily': 'comicsansms',
                                'fontsize': 25,
                                'color off':(255,255,0),
                                'color on': (0,255,0),
                                'color' : (255,255,0),
                                'over' : (105,105,105),
                                'overed' : False,
                                'position': (1150,150)}

        buttons['Grid'] = {'status' : False,
                           'fontfamily': 'comicsansms',
                           'fontsize': 25,
                           'color off':(255,255,0),
                           'color on': (0,255,0),
                           'color' : (255,255,0),
                           'over' : (105,105,105),
                           'overed' : False,
                           'position': (1150,250)}

        buttons['Save'] = {'status' : False,
                           'fontfamily': 'comicsansms',
                           'fontsize': 25,
                           'color off':(255,255,0),
                           'color on': (0,255,0),
                           'color' : (255,255,0),
                           'over' : (105,105,105),
                           'overed' : False,
                           'position': (1150,350)}

        selected = "Add Block"

        char_dict = {"Add Block": "X",
                     "Remove Block":"E"}

        done = False

        while not done:
            t0 = time.time()
            i = j = -1
            
            #Background
                          
            Editor.data2image(data, image, 32, buttons['Grid']['status'])
                
            bg = pygame.image.load('background_edited.png')
            gc.screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            mouseover = ""
            for but in buttons:
                buttons[but]['overed'] = False
                
            if x > 992 and x < 1280:
                if y > 0 and y < 100:
                    buttons['Add Block']['overed'] = True
                    mouseover = 'Add Block'
                    
                if y > 100 and y < 200:
                    buttons['Remove Block']['overed'] = True
                    mouseover = 'Remove Block'

                if y > 200 and y < 300:
                    buttons['Grid']['overed'] = True
                    mouseover = 'Grid'
                    
                if y > 300 and y < 400:
                    buttons['Save']['overed'] = True
                    mouseover = 'Save'

            elif x < 992:
                i = y // 32
                j = x // 32
                
            for event in pygame.event.get():
                #Escape condition        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

                #Mouse clic event
                if event.type == pygame.MOUSEBUTTONUP:
                    if not mouseover == "":
                        if selected == 'Grid' and mouseover == 'Grid':
                            buttons['Grid']['status'] = False
                            break
                        for but in buttons:
                            buttons[but]['status'] = False
                            
                        buttons[mouseover]['status'] = True
                        selected = mouseover
                    if not i == -1:
                        data[i][j] = char_dict[selected]
                    
            #Options
            for but in buttons:
                if buttons[but]['overed']:
                    pygame.draw.rect(gc.screen, buttons[but]['over'],
                                     (buttons[but]['position'][0]-158,
                                      buttons[but]['position'][1]-50,
                                      288,
                                      100))
                if buttons[but]['status']:
                    color = buttons[but]['color on']
                else:
                    color = buttons[but]['color off']
                font = pygame.font.SysFont(buttons[but]['fontfamily'],
                                           buttons[but]['fontsize'])
                text = font.render(but, False, color)
                gc.screen.blit(text,(buttons[but]['position'][0] - text.get_width() // 2,
                                       buttons[but]['position'][1] - text.get_height() // 2))
                
            
            pygame.display.flip()

            if selected == 'Save':
                f = open('edited_map.txt','w')
                for d in data:
                    f.write("".join(d)+'\n')
                f.close()
                done = True

            dt = time.time() - t0
            wait = 1/30 - dt
            if wait > 0:
                time.sleep(wait)
