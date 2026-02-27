import pygame

BACKGROUND_CHECKER_BLUE = pygame.Color(224, 218, 254)
BACKGROUND_CHECKER_WHITE = pygame.Color(249, 248, 255)
BG_COLOR = pygame.Color(177,172,255)
SAFE_AREA_COLOR = pygame.Color(114,222,110)
BG_SQUARE_LENGTH = 60 

def create_level(screen,safeAreas,finishArea,startPosition = pygame.Vector2(0,0),x=0,y=0):
    if(x == 0 or y == 0):
        raise ValueError("[create_level] one or more args not given!")
    # create the matrix of checkered squares off of the size 
    for x_count in range(0,x):
        for y_count in range(0,y):
            currentRect = pygame.Rect(startPosition.x+ x_count*BG_SQUARE_LENGTH,
            startPosition.y+y_count*BG_SQUARE_LENGTH,BG_SQUARE_LENGTH,BG_SQUARE_LENGTH)
            if (x_count+ y_count) % 2 ==0:
                charColor = BACKGROUND_CHECKER_BLUE
            else:
                charColor = BACKGROUND_CHECKER_WHITE
            pygame.draw.rect(screen,charColor,currentRect)

    #create the level spawn (safe area)
    for i in range(len(safeAreas)):
        pygame.draw.rect(screen,SAFE_AREA_COLOR,safeAreas[i])
    
    #create the level finish box (safe area) --> takes the player to the next level once all coins are collected
    pygame.draw.rect(screen,SAFE_AREA_COLOR,finishArea)