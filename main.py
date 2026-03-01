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
    
    def update(self, dt, walls):

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

        # Move X axis then resolve collisions
        self.pos.x += self.velocity.x * PLAYER_SPEED * dt
        self.rect.x = int(self.pos.x)
        for wall in pg.sprite.spritecollide(self, walls, False):
            if self.velocity.x > 0:
                self.rect.right = wall.rect.left
            elif self.velocity.x < 0:
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.x

        # Move Y axis then resolve collisions
        self.pos.y += self.velocity.y * PLAYER_SPEED * dt
        self.rect.y = int(self.pos.y)
        for wall in pg.sprite.spritecollide(self, walls, False):
            if self.velocity.y > 0:
                self.rect.bottom = wall.rect.top
            elif self.velocity.y < 0:
                self.rect.top = wall.rect.bottom
            self.pos.y = self.rect.y

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
    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((rect.width, rect.height))
        self.rect = rect.copy()

class Enemy(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.anchor_pos = pg.math.Vector2(x, y)
        self.image, self.rect = LevelFunctions.load_image('enemy.png', 1, (48, 48))
        self.pos = pg.Vector2(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        
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




# get all rectangles on screen from the pixel art image 
rectsOnScreen = LevelFunctions.convertImageToScreen(screen,'./assets/level1map.png')
newBg = pg.Surface(screen.get_size()).convert()
newBg.fill(LevelFunctions.BACKGROUND_COLOR)

for (color, rect) in rectsOnScreen:
    pg.draw.rect(newBg, color, rect)

black_tuples = [(color, rect) for color, rect in rectsOnScreen if color == LevelFunctions.BACKGROUND_BLACK]

walls = list(map(lambda obj: Wall(obj[1]), black_tuples))

lvl1Enemies = pg.sprite.Group()
 
player = Player(screen.get_width()/2,screen.get_height()/2)   
match LEVEL:
    case 1: 
        #create enemies and create level 
        enemy1 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 + 45,3,270,0)
        enemy2 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -15,3,270,1)
        enemy3 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -75,3,270,0)
        enemy4 = SinEnemy(screen.get_width()/2 - 25, screen.get_height()/2 -135,3,270,1)
        # get all rectangles on screen from the pixel art image 
        lvl1Enemies.add(enemy1)
        lvl1Enemies.add(enemy2)
        lvl1Enemies.add(enemy3)
        lvl1Enemies.add(enemy4)
        
        rectsOnScreen = LevelFunctions.convertImageToScreen(screen,'./assets/level1map.png')
        newBg = pg.Surface(screen.get_size()).convert()
        newBg.fill(pg.Color(177,172,255))

        for (color, rect) in rectsOnScreen:
            if(color == LevelFunctions.SAFE_AREA_COLOR and not playerSpawned):
                print("SAFE AREA FOUND")
                playerSpawned = True
                player.pos = pg.Vector2(rect.left, rect.top)

                #TODO add wall logic call 
                
            pg.draw.rect(newBg, color, rect)


        
    case _ :
        raise "NO LEVEL SELECTED"

rectsOnScreen = LevelFunctions.convertImageToScreen(screen,'./assets/level1map.png')
LevelFunctions.cut_walls(newBg, rectsOnScreen)
########################################################
# Initialize Sprites
########################################################


# spawns coin in the center of the screen
coin = Coin(screen.get_width()/2, screen.get_height()/2)


# group all sprites together
allsprites = pg.sprite.Group((player, coin))


allwalls = pg.sprite.Group()
for wall in walls:
    allwalls.add(wall)
    
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
    #Update and Draw All Walls group

    #update player and coin separate (even though they share group)
    player.update(dt, allwalls)
    coin.update()

    #Update and Draw LVL 1 Enemies Group
    lvl1Enemies.update()
    lvl1Enemies.draw(screen)

    #Update and Draw All Sprites group (player and coin)
    allsprites.draw(screen)


    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # independent physics.
    dt = clock.tick(60) / 1000 # dt is delta time in seconds since last frame, used for framerate-


pg.quit()