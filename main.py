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
player_spawn = pg.Vector2(0,0)
playerSpawned = False
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


class Enemy(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.anchor_pos = pg.math.Vector2(x, y)
        self.image, self.rect = LevelFunctions.load_image('enemy.png', 1, (48, 48))
        
    def update(self):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x +  math.sin(t * 3) * 300, self.anchor_pos.y )
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class SinEnemy(Enemy):

    def __init__(self, x, y,frequency,amplitude,delay): 
        super().__init__(x,y)
        self.amplitude = amplitude
        self.delay = delay  
        self.frequency = frequency
    
    #Override 
    def update(self):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x +  math.sin((t-(self.delay)) * self.frequency) * self.amplitude, self.anchor_pos.y )
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

enemies = []   
player = Player(screen.get_width()/2,screen.get_height()/2)   
match LEVEL:
    case 1: 
        #create enemies and create level 
        enemy1 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 + 45,3,270,0)
        enemy2 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -10,3,270,1)
        enemy3 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -65,3,270,0)
        enemy4 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -120,3,270,1)
        # get all rectangles on screen from the pixel art image 
        enemies.append(enemy1)
        enemies.append(enemy2)
        enemies.append(enemy3)
        enemies.append(enemy4)
        rectsOnScreen = LevelFunctions.convertImageToScreen(screen,'./assets/level1map.png')
        newBg = pg.Surface(screen.get_size()).convert()
        newBg.fill(pg.Color(177,172,255))

        for (color, rect,(pos_x,pos_y)) in rectsOnScreen:
            if(color == LevelFunctions.SAFE_AREA_COLOR and not playerSpawned):
                print("SAFE AREA FOUND")
                playerSpawned = True
                player.pos = pg.Vector2(rect.left, rect.top)

                #TODO add wall logic call 

                
            pg.draw.rect(newBg, color, rect)


        
    case _ :
        raise "NO LEVEL SELECTED"
########################################################
# Initialize Sprites
########################################################


# spawns coin in the center of the screen
coin = Coin(screen.get_width()/2, screen.get_height()/2)

allsprites = pg.sprite.RenderPlain((player, coin)) # creating a group 

for i in range(len(enemies)): # add all enemies to sprite group
    allsprites.add(enemies[i])



    
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