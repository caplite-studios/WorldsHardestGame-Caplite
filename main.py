# Example file showing a circle moving on screen
import os
import pygame as pg
import math
# pygame setup
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
dt = 0

# Define global variables 
LEVEL = 1

import LevelFunctions
PLAYER_COLOR = pg.Color(251,3,1)
SPEED_INT = 4
PLAYER_SPEED = SPEED_INT * 100

# Define helper functions

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")

def load_image(name, scale=1, size=None):
    fullname = os.path.join(assets_dir, name)
    image = pg.image.load(fullname).convert_alpha()
    if size:
        image = pg.transform.scale(image, size)
    elif scale != 1:
        size = image.get_size()
        image = pg.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    return image, image.get_rect()



player_img= pg.image.load('./assets/Character.png').convert_alpha()
PLAYER_IMG = pg.transform.scale(player_img, (48, 48))

coin_img= pg.image.load('./assets/coin.png').convert_alpha()
COIN_IMG = pg.transform.scale(coin_img, (48, 48))

#Define our player sprites

class Player(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Character.png', 1, (48, 48))
        self.rect.topleft = (x, y)
        self.pos = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2(0, 0)
    
    def update(self):
        
        # set the player movement vector to zero before handling inputs
        self.velocity = pg.Vector2(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity.y -= 1
        if keys[pg.K_s]:
            self.velocity.y += 1
        if keys[pg.K_a]:
            self.velocity.x -= 1 
        if keys[pg.K_d]:
            self.velocity.x += 1
        #when movement vector greater than 1 (for diagonals)
        if (self.velocity.length() > 1):
            self.velocity.normalize_ip()
        self.pos += self.velocity * PLAYER_SPEED * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class Coin(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('coin.png', 1, (48, 48))
        self.rect.topleft = (x, y)
        self.anchor_pos = pg.math.Vector2(x, y)
        self.pos = pg.math.Vector2(x, y)

    def update(self):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x, self.anchor_pos.y + math.sin(t * 2.5) * 15)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))


# TEST CODE - REMOVE ALL REFERENCES
font = pg.font.SysFont("comicsans", 20)
txt = pg.font.Font.render(font, "Level 1", True, (0, 0, 0))
# END TEST CODE


# spawns player in the middle left of screen
player = Player(screen.get_width()/2, screen.get_height()/2)

# spawns coin in the center of the screen
coin = Coin(screen.get_width()/2, screen.get_height()/2)

allsprites = pg.sprite.RenderPlain((player, coin))

match LEVEL: # change player spawn position based on the level number
    case 1:
        # spawn player in the middle of the screen, all the way to the left
        player_pos = pg.Vector2(0, screen.get_height() / 2)

#GAME LOOP
time = 0
while running:
    time = pg.time.get_ticks() / 1000 

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
                safeAreas = [pg.Rect(
                    -20,
                    lvl1StartY,
                    LevelFunctions.BG_SQUARE_LENGTH * 2,
                    LevelFunctions.BG_SQUARE_LENGTH * lvl1Height
                )]
                finishArea = pg.Rect(
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
                    pg.Vector2(lvl1StartX,lvl1StartY),
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
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_m]:
        running = False

    allsprites.update()

    allsprites.draw(screen)

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # independent physics.
    dt = clock.tick(60) / 1000 # dt is delta time in seconds since last frame, used for framerate-


pg.quit()