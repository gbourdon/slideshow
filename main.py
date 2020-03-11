import sys
import os
from datetime import datetime
import pygame
from time import sleep
from utilities import *

def main(argv):
    dimns = (1920, 1080)
    config = load_config('config')
    startTime = datetime.now()
    position = 0
    images = []
    background_color = (config['background_red'], config['background_green'], config['background_blue'])

    images = load_files()
    drives = get_drives()

    disp = pygame.display.set_mode(dimns, pygame.FULLSCREEN)
    pic = show_image(os.path.join('.', 'welcome.jpg'), disp)

    pygame.mouse.set_visible(0)
    pygame.display.set_caption('Slideshow')

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit() # Yes, THIS BLOODY WORKS, PYLINT!!!
            if pygame.mouse.get_pressed()[2]: sys.exit() # Exits if right click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: sys.exit()
                #if event.key == pygame.K_PLUS: config['time'] += 10
                #if event.key == pygame.K_PLUS: config['time'] -= 10
                if event.key == pygame.K_r:
                    position = 0
                    images = load_files()
        if len(list(filter(lambda x: x not in drives, get_drives()))) != 0:
            print(get_drives())
            position = 0
            images = load_files()
            #drives = get_drives() # Is it possible to remove this line?

        if len(get_drives()) != len(drives):
            print("HI!")
            drives = get_drives()
        
        try:
            if (((datetime.now() - startTime).seconds % config['time']) == 0): # Need to set it so that it only evals once
                position = (position + 1) % (len(images))
                disp.fill(background_color)
                pic = show_image(images[position], disp)
                sleep(1) # Prevents the program from glitching out with changing images. This is why it might take a (literal) second to do a command after switching an image.
        except pygame.error as error:
            print(error)
            position = 0
            images.clear()
            images.append(os.path.join('.', 'error.jpg'))
            if len(load_files()) != 0:
                images = load_files()
    pass

if __name__ == "__main__":
    main(sys.argv)
