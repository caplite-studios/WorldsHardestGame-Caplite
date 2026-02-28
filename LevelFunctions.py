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
SAFE_AREA_COLOR = pg.Color(114,222,110)
BG_SQUARE_LENGTH = 60 
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

#load source images 
#BG_SQ_BLACK = load_image('blackBox.png',1,(48,48))

def create_level(
    screen,
    safeAreas,
    finishArea,
    startPosition = pg.Vector2(0,0),
    x=0,
    y=0
):
    '''
    Given a width and height, and
    '''
    if x == 0 or y == 0:
        raise ValueError("[create_level] one or more args not given!")
    # create the matrix of checkered squares off of the size 
    for x_count in range(0,x):
        for y_count in range(0,y):
            currentRect = pg.Rect(
                startPosition.x + x_count * BG_SQUARE_LENGTH,
                startPosition.y + y_count * BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH
            )
            if (x_count + y_count) % 2 == 0:
                
                charColor = BACKGROUND_CHECKER_BLUE
            else:
                charColor = BACKGROUND_CHECKER_WHITE
            pg.draw.rect(screen,charColor,currentRect)

    #create the level spawn (safe area)
    for i in range(len(safeAreas)):
        pg.draw.rect(screen,SAFE_AREA_COLOR,safeAreas[i])
    
    #create the level finish box (safe area) --> takes the player to the next level once all coins are collected
    pg.draw.rect(screen,SAFE_AREA_COLOR,finishArea)




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
    returnList: list[tuple[pg.Color, pg.Rect]] = []
    for x in range(width):
        for y in range(height):
            pixel_value  = pixels[x,y]
            r,g,b,a = pixel_value

            if(a== 0): # pixel is casted to a transparent pixel
                continue 
                
            #print(f'alpha of pixel ({x},{y}) = {a} ')
            currentRect = pg.Rect(
                ORIENTATION_OFFSET_X + x * BG_SQUARE_LENGTH,
                ORIENTATION_OFFSET_Y + y * BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH
            )
            currColor = pg.Color(r,g,b)
            returnList.append((currColor,currentRect))
    return returnList
