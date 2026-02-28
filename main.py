import os
import pygame as pg
import math
import LevelFunctions
########################################################
# Define global variables 
########################################################
LEVEL = 1
PLAYER_COLOR = pg.Color(251,3,1)
SPEED_INT = 4
PLAYER_SPEED = SPEED_INT * 100
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = SCREEN_WIDTH

########################################################
# Setting up screen display  
########################################################
pg.init()
screen = pg.display.set_mode((1440, 1440))
clock = pg.time.Clock()
running = True
dt = 0

# Define the background
background = pg.Surface(screen.get_size()).convert()
background.fill(LevelFunctions.BACKGROUND_COLOR)


# Render blank background while loading happens
screen.blit(background, (0, 0))
pg.display.flip()


main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")



########################################################
# Define our player sprites
########################################################
class Player(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = LevelFunctions.load_image('Character.png', 1, (48, 48))
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
        self.image, self.rect = LevelFunctions.load_image('coin.png', 1, (48, 48))
        self.rect.topleft = (x, y)
        self.anchor_pos = pg.math.Vector2(x, y)
        self.pos = pg.math.Vector2(x, y)

    def update(self):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x, self.anchor_pos.y + math.sin(t * 2.5) * 15)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class Wall(pg.sprite.Sprite):


    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(x, y)
        self.rect = self.image.get_rect()

########################################################
# Initialize Sprites
########################################################
# spawns player in the middle left of screen
player = Player(screen.get_width()/2, screen.get_height()/2)

# spawns coin in the center of the screen
coin = Coin(screen.get_width()/2, screen.get_height()/2)

allsprites = pg.sprite.RenderPlain((player, coin))

# get all rectangles on screen from the pixel art image 
rectsOnScreen = LevelFunctions.convertImageToScreen(screen,'./assets/level1map.png')
newBg = pg.Surface(screen.get_size()).convert()
newBg.fill(LevelFunctions.BACKGROUND_COLOR)

for (color, rect) in rectsOnScreen:
    pg.draw.rect(newBg, color, rect)

    
########################################################
#GAME LOOP
########################################################
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(LevelFunctions.BACKGROUND_COLOR)
    

    # poll for events
    # pygame.QUIT event means the user clicked red X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_m]:
        running = False

    screen.blit(newBg,(0,0))
    allsprites.update()

    allsprites.draw(screen)


    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # independent physics.
    dt = clock.tick(60) / 1000 # dt is delta time in seconds since last frame, used for framerate-


pg.quit()