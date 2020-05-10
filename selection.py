import cv2
import pygame
import os
import time

class Selection:

    def start(gc):
        #clear screen
        pygame.draw.rect(gc.screen, (0,0,0),(0,0,1280,900))
        pygame.display.flip()

        directories = os.listdir("sprites")
        char = []
        for d in directories:
            if d.find('.') == -1:
                char.append(d)

        img = {}
        
        x = 32
        y = 64

        converter = {0: "image",
                     1: "anim_1",
                     2: "anim_2"}
        
        for idx, i in enumerate(char):
            im = cv2.imread("sprites/"+i+"/down_0.png")
            resized = cv2.resize(im, (64,64), interpolation = cv2.INTER_AREA)
            cv2.imwrite("sprites/"+i+"/resized_0.png", resized)
            img[i] = {"image": pygame.image.load("sprites/"+i+"/resized_0.png")}

            im = cv2.imread("sprites/"+i+"/down_1.png")
            resized = cv2.resize(im, (64,64), interpolation = cv2.INTER_AREA)
            cv2.imwrite("sprites/"+i+"/resized_1.png", resized)
            img[i]["anim_1"] = pygame.image.load("sprites/"+i+"/resized_1.png")

            im = cv2.imread("sprites/"+i+"/down_2.png")
            resized = cv2.resize(im, (64,64), interpolation = cv2.INTER_AREA)
            cv2.imwrite("sprites/"+i+"/resized_2.png", resized)
            img[i]["anim_2"] = pygame.image.load("sprites/"+i+"/resized_2.png")
            img[i]['x'] = x
            img[i]['y'] = y
            img[i]['status'] = 0
            img[i]['accu'] = 0
            img[i]['mover'] = False
            img[i]['selected'] = False
            
            x += 128
            if x > 1100:
                x = 32
                y += 128
                
        select = None
        done = False
        
        try:
            f = open('char_selection.txt')
            select = f.read().replace('\n','')
            img[select]['selected'] = True
        except OSError as err:
            pass
        
        while not done:
            t0 = time.time()
            mouse_click = False
            pygame.draw.rect(gc.screen, (0,0,0),(0,0,1280,900))
            for event in pygame.event.get():
                #Escape condition        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                #Mouse Click event
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = True

            xm, ym = pygame.mouse.get_pos()
            for i in img:
                img[i]['mover'] = False
                if xm > img[i]['x'] - 10 and xm < img[i]['x'] + 74:
                    if ym > img[i]['y'] - 10 and ym < img[i]['y'] + 74:
                        pygame.draw.rect(gc.screen, (255,255,255),(img[i]['x'] - 10, img[i]['y']-10 ,84, 84))
                        img[i]['mover'] = True
                        
                if img[i]['mover'] and mouse_click:
                    if not select == None:
                        img[select]['selected'] = False
                    img[i]['selected'] = True
                    select = i

                if img[i]['selected']:
                    pygame.draw.rect(gc.screen, (255,255,0),(img[i]['x'] - 10, img[i]['y']-10 ,84, 84))
                    
                gc.screen.blit(img[i][converter[img[i]['status']]], (img[i]['x'], img[i]['y']))
                img[i]['accu'] += 1
                if img[i]['accu'] % 7 == 0:
                    img[i]['status'] += 1
                if img[i]['accu'] > 21:
                    img[i]['accu'] = 0
                if img[i]['status'] > 2:
                    img[i]['status'] = 0
            pygame.display.flip()

            dt = t0 - time.time()
            time2wait = 1/30 - dt
            if time2wait > 0:
                time.sleep(time2wait)


        #Saving the selection
        if not select == None:
            f = open('char_selection.txt','w')
            f.write(select)
            f.close()
