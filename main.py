# Example file showing a circle moving on screen
import pygame
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#define global variables 
LEVEL = 1

import LevelFunctions
PLAYER_COLOR = pygame.Color(251,3,1)
SPEED_INT = 4
PLAYER_SPEED = SPEED_INT * 100


player_img= pygame.image.load('./assets/Character.png').convert_alpha()
PLAYER_IMG = pygame.transform.scale(player_img, (48, 48))

coin_img= pygame.image.load('./assets/coin.png').convert_alpha()
COIN_IMG = pygame.transform.scale(coin_img, (48, 48))

#Define our player sprites


# TEST CODE - REMOVE ALL REFERENCES
font = pygame.font.SysFont("comicsans", 20)
txt = pygame.font.Font.render(font, "Level 1", True, (0, 0, 0))
# END TEST CODE


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) # center by default
movement = pygame.Vector2(0, 0)

#initial coin position (before movement function in the loop)
coin_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

match LEVEL: # change player spawn position based on the level number
    case 1:
        # spawn player in the middle of the screen, all the way to the left
        player_pos = pygame.Vector2(0, screen.get_height() / 2)

#GAME LOOP
time = 0
while running:
    time = pygame.time.get_ticks() / 1000 

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(LevelFunctions.BG_COLOR)
    
    match LEVEL: # define our level
        case 1: # the user selects level 1 
            try:
                lvl1Width = 17
                lvl1Height = 6
                lvl1StartX = 100
                # centers the map height wise?
                lvl1StartY = screen.get_height() / 2 - LevelFunctions.BG_SQUARE_LENGTH * lvl1Height / 2
                safeAreas = [pygame.Rect(
                    -20,
                    lvl1StartY,
                    LevelFunctions.BG_SQUARE_LENGTH * 2,
                    LevelFunctions.BG_SQUARE_LENGTH * lvl1Height
                )]
                finishArea = pygame.Rect(
                    LevelFunctions.BG_SQUARE_LENGTH*lvl1Width + 100,
                    lvl1StartY,
                    LevelFunctions.BG_SQUARE_LENGTH * 2,
                    LevelFunctions.BG_SQUARE_LENGTH * lvl1Height
                )

                # creates the checkered background tiles of white/blue tiles 
                LevelFunctions.create_level(
                    screen,
                    safeAreas,
                    finishArea,
                    pygame.Vector2(lvl1StartX,lvl1StartY),
                    lvl1Width,
                    lvl1Height
                )

                # TODO: REMOVE To truly center the text, set to sw/2 - tw/2
                screen.blit(txt, (screen.get_width() / 2 - txt.get_width() / 2, screen.get_height() / 10))

            except Exception as E:
                print(E)
        case _:
            print(f"LEVEL NOT FOUND")

    '''
    ---- IF YOU WANT TO RENDER ANYTHING NEW FOR LEVEL 1 (ENEMY CIRCLE,WALLS,etc.) DO IT HERE ---- 
    START TODO
    '''



    '''
    END TODO 
    '''


    # poll for events
    # pygame.QUIT event means the user clicked red X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # draws player sprite (use blit for sprite)
    screen.blit(PLAYER_IMG, player_pos)

    # function to move coin in a sine wave 
    coin_position.y= screen.get_height() / 2 + math.sin(time * 2.5) * 15 

    # draws coin sprite
    screen.blit(COIN_IMG, coin_position)  

    # set the player movement vector to zero before handling inputs
    movement = pygame.Vector2(0,0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        movement.y -= 1
    if keys[pygame.K_s]:
        movement.y += 1
    if keys[pygame.K_a]:
        movement.x -= 1 
    if keys[pygame.K_d]:
        movement.x += 1
    # if the user hits m, it exits out of the game (FOR DEBUGGING ONLY)
    if keys[pygame.K_m]:
        running = False


    #when movement vector greater than 1 (for diagonals)
    if (movement.length() > 1):
        movement.normalize_ip()
    
    player_pos += movement * PLAYER_SPEED * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # independent physics.
    dt = clock.tick(60) / 1000 # dt is delta time in seconds since last frame, used for framerate-


pygame.quit()