import pygame as pg
import os
from PIL import Image

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")


BACKGROUND_CHECKER_BLUE = pg.Color(224, 218, 254)
BACKGROUND_CHECKER_WHITE = pg.Color(249, 248, 255)
BACKGROUND_BLACK = pg.Color(0,0,0)
BACKGROUND_GREEN = pg.Color(0,230,0)
BACKGROUND_COLOR = pg.Color(177,172,255)
BG_SQUARE_LENGTH = 60 
SAFE_AREA_COLOR = pg.Color(51, 232, 140)

ORIENTATION_OFFSET_X = -300
ORIENTATION_OFFSET_Y = -200

def load_image(name, scale=1, size=None):
    fullname = os.path.join(assets_dir, name)
    image = pg.image.load(fullname).convert_alpha()
    if size:
        image = pg.transform.scale(image, size)
    elif scale != 1:
        size = image.get_size()
        image = pg.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    return image, image.get_rect()

"""
Given an image (32x32)
0. Open the image 
1. iterate through each pixel of the image  
2. draw rect (size 60) at coordinate scaled up 
"""
def convertImageToScreen(screen=None, src=''):
    if(screen ==None):
        raise ValueError("[convertImageToScreen]  not given!")
    if(src ==''):
        raise ValueError("[convertImageToScreen] src not given!")
    img = Image.open(src).convert("RGBA")
    width,height =  img.size
    pixels = img.load()
    returnList = []
    for x in range(width):
        for y in range(height):
            pixel_value  = pixels[x,y]
            r,g,b,a = pixel_value

            if(a== 0): # pixel is casted to a transparent pixel
                continue 
            
            # if(x ==9 and y==13):
            #     print(f'colors of pixel ({x},{y}) = {r,g,b,a} ')
            currentRect = pg.Rect(
                ORIENTATION_OFFSET_X + x * BG_SQUARE_LENGTH,
                ORIENTATION_OFFSET_Y + y * BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH
            )
            currColor = pg.Color(r,g,b,a)
            returnList.append((currColor,currentRect))
    return returnList
