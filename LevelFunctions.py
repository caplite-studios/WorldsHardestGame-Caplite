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
def convertImageToScreen(screen=None, src='', square_length=BG_SQUARE_LENGTH):
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

            # if(a== 0): # pixel is casted to a transparent pixel
            #     continue 
            
            # if(x ==9 and y==13):
            #     print(f'colors of pixel ({x},{y}) = {r,g,b,a} ')
            currentRect = pg.Rect(
                ORIENTATION_OFFSET_X + x * square_length,
                ORIENTATION_OFFSET_Y + y * square_length,
                square_length,
                square_length
            )
            currColor = pg.Color(r,g,b,a) if a != 0 else BACKGROUND_COLOR
            returnList.append((currColor,currentRect))
    return returnList

def cut_walls(surface: pg.surface.Surface, rects: list[tuple[pg.Color, pg.Rect]], square_length=BG_SQUARE_LENGTH):
    LINE_WIDTH = 3

    def non_playable(color):
        return color == BACKGROUND_COLOR or color == BACKGROUND_BLACK

    # Build position lookup so we can find neighbors in O(1)
    color_map = {(r.left, r.top): color for color, r in rects}

    for color, rect in rects:
        if not non_playable(color):
            continue

        # Erase wall — fill with plain background
        pg.draw.rect(surface, BACKGROUND_COLOR, rect)

        # For each cardinal neighbor, draw a border line if it faces a playable square
        cardinal_neighbors = {
            'N': (rect.left, rect.top - square_length),
            'S': (rect.left, rect.top + square_length),
            'E': (rect.left + square_length, rect.top),
            'W': (rect.left - square_length, rect.top),
        }
        for direction, pos in cardinal_neighbors.items():
            neighbor_color = color_map.get(pos)
            # No neighbor (off-map) or neighbor is also non-playable → no line
            if neighbor_color is None or non_playable(neighbor_color):
                continue
            # Neighbor is playable → draw border on this edge
            if direction == 'N':
                pg.draw.line(surface, BACKGROUND_BLACK, rect.topleft, rect.topright, LINE_WIDTH)
            elif direction == 'S':
                pg.draw.line(surface, BACKGROUND_BLACK, rect.bottomleft, rect.bottomright, LINE_WIDTH)
            elif direction == 'E':
                pg.draw.line(surface, BACKGROUND_BLACK, rect.topright, rect.bottomright, LINE_WIDTH)
            elif direction == 'W':
                pg.draw.line(surface, BACKGROUND_BLACK, rect.topleft, rect.bottomleft, LINE_WIDTH)


        



    
