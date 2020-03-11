import sys
import os
from datetime import datetime
import pygame
from time import sleep

def show_image(img, screen):
    """Displays an image at the required aspect ratio (Disp) \n
    Img: The path to the image \n
    Disp: The display used to display the image"""
    dimns = screen.get_rect().size
    pic = pygame.image.load(img).convert()
    pic = aspect_scale(pic, dimns)
    picrect = pic.get_rect(centerx = screen.get_width()/2)
    screen.blit(pic, picrect)
    pygame.display.update()
    return pic

def aspect_scale(img, box):
    """aspect_scale.py - Scaling surfaces keeping their aspect ratio
    Raiser, Frank - Sep 6, 2k++ (Modified to work with project)
    crashchaos at gmx.net

    This is a pretty simple and basic function that is a kind of
    enhancement to pygame.transform.scale. It scales a surface
    (using pygame.transform.scale) but keeps the surface's aspect
    ratio intact. So you will not get distorted images after scaling.
    A pretty basic functionality indeed but also a pretty useful one.

    Usage:
    is straightforward.. just create your surface and pass it as
    first parameter. Then pass the width and height of the box to
    which size your surface shall be scaled as a tuple in the second
    parameter. The aspect_scale method will then return you the scaled
    surface (which does not neccessarily have the size of the specified
    box of course)

    Dependency:
    a pygame version supporting pygame.transform (pygame-1.1+)
    """
    bx, by = box
    ix, iy = img.get_rect().size

    #print(img.get_rect().size)

    if ix == iy:
        scale_factor = bx/float(iy)

    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    elif ix == iy:
        sy = sx = by
    else:
        # fit to height
        scale_factor = bx/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))

def get_files(path):
    """Returns the files in directory path (Without path) (List) \n
    Path: The path to the directory (String)
    """
    f = []
    for (_, _, filenames) in os.walk(path):
        for files in filenames:
            f.append(os.path.join(path, files))
        break
    return f

def get_drives():
    f = []
    for _,drives,_ in os.walk(os.path.join('/', 'media', 'pi')):
        f.extend(drives)
        break
    return f

def load_files():
    """Loads the required files (List)"""
    f = []
    if sys.platform == 'linux': # Detects if it is using Linux (Might have to modify to work on something other than a Pi)
        for _,drives,_ in os.walk(os.path.join('/', 'media', 'pi')):
            for drive in drives:
                for _,folders,_ in os.walk(os.path.join('/', 'media', 'pi', drive)):
                    for folder in folders:
                        if folder.lower() == "images":
                            for directory, _, _ in os.walk(os.path.join('/', 'media', 'pi', drive, folder)):
                                f.extend(get_files(directory))
                            f.extend(get_files(os.path.join('/', 'media', 'pi', drive, folder)))
                    break
            break
    if len(f) == 0:
        print("No images found in drive or using a non-pi system, using default images")
        f.extend(get_files(os.path.join('.','images')))
    return f

def load_config(config):
    """Returns the configuration options (Dict, (String, int)) \n
    Config: The path to the file containing values in a 'k, v' format (String)
    """
    outd = {}
    with open(config, 'r') as f:
        for line in f:
            din = line.split(', ')
            outd[din[0]] = int(din[1])
    return outd