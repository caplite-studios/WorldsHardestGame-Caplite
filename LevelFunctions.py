import pygame as pg

BACKGROUND_CHECKER_BLUE = pg.Color(224, 218, 254)
BACKGROUND_CHECKER_WHITE = pg.Color(249, 248, 255)
BG_COLOR = pg.Color(177,172,255)
SAFE_AREA_COLOR = pg.Color(114,222,110)
BG_SQUARE_LENGTH = 60 

def create_level(
    screen,
    safe_areas,
    finish_area,
    start_position = pg.Vector2(0,0),
    x=0,
    y=0
):
    '''
    Creates a game level by 
        - drawing a checkered grid from the start position 
            and extending to the specified size (x,y) onto the surface (screen)
        - drawing all the safe areas onto the screen
        - drawing the finish area onto the screen
    
    Args:
        screen (pygame.Surface): surface (screen) to draw everything onto
        safe_areas (list[pygame.Rect]): array of Rects that will be drawn directly onto the screen
        finish_area (pygame.Rect): Rect that will be drawn directly onto the screen
        start_position (pygame.math.Vector2): Vector representing the start position of drawing the checkered grid
        x (integer): width of the desired checkered box
        y (integer): height of the desired checkered box

    Returns:
        None
    '''
    if x == 0 or y == 0:
        raise ValueError("[create_level] one or more args not given!")
    # create the matrix of checkered squares off of the size 
    for x_count in range(0,x):
        for y_count in range(0,y):
            currentRect = pg.Rect(
                start_position.x + x_count * BG_SQUARE_LENGTH,
                start_position.y + y_count * BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH,
                BG_SQUARE_LENGTH
            )
            if (x_count + y_count) % 2 == 0:
                charColor = BACKGROUND_CHECKER_BLUE
            else:
                charColor = BACKGROUND_CHECKER_WHITE
            pg.draw.rect(screen,charColor,currentRect)

    #create the level spawn (safe area)
    for i in range(len(safe_areas)):
        pg.draw.rect(screen,SAFE_AREA_COLOR,safe_areas[i])
    
    #create the level finish box (safe area) --> takes the player to the next level once all coins are collected
    pg.draw.rect(screen,SAFE_AREA_COLOR,finish_area)