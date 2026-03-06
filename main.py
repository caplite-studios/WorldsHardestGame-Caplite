import os
from unittest import case
import pygame as pg
import math
import LevelFunctions

########################################################
# Define global variables
########################################################
level = 2
currentLevelSafeArea: tuple[pg.math.Vector2, pg.math.Vector2] = tuple[pg.math.Vector2(0,0),pg.math.Vector2(1,1)] 
listOfSafeAreaBoxes: list[pg.math.Vector2] = []
safeRectTransition = None
rectsOnScreen = []
numDeaths = 0
splash_screen_time_seconds = 2
PLAYER_COLOR = pg.Color(251, 3, 1)
SPEED_INT = 4
PLAYER_SPEED = SPEED_INT * 100

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = SCREEN_WIDTH

########################################################
# Setting up screen display
########################################################
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
background = pg.Surface(screen.get_size()).convert()
background.fill(LevelFunctions.BACKGROUND_COLOR)
pg.display.set_caption("The World's Most Game")

screen.blit(background, (0, 0))
pg.display.flip()

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")

# Load splash screen
splash_img = pg.image.load(os.path.join(assets_dir, 'worlds_most_game_splash.png')).convert()
splash_img = pg.transform.scale(splash_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create dimmed version for menu background
splash_dimmed = splash_img.copy()
dim_overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
dim_overlay.fill((0, 0, 0))
dim_overlay.set_alpha(120)
splash_dimmed.blit(dim_overlay, (0, 0))


def get_font(size):
    return pg.font.SysFont('comicsansms', size)



########################################################
# System utils
########################################################

class LevelTransition():
    def __init__(self,currentLevel,rect):
        pg.sprite.Sprite.__init__(self)
        self.rect = rect
        self.pos = pg.Vector2(self.rect.left, self.rect.top)
        self.currentLevel= currentLevel


class UIRect():

    def __init__(self, pos, font, text_input, foreground, background):
        self.x_pos = pos[1]
        self.y_pos = pos[0]
        self.font = font
        self.foreground = foreground
        self.background = background
        self.text_input = text_input
        self.surface = self.font.render(self.text_input, True, foreground, background)
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.surface, self.rect)

    # def change_color(self, pos):
    #     x, y = pos
    #     new_bg = self.background
    #     if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
    #         new_bg.a = 100
    #     else:
    #         new_bg.a = 20
    #     self.surface = self.font.render(self.text_input, True, self.foreground, new_bg)
class Button():

    def __init__(self, pos, font, text_input, foreground, background):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.foreground = foreground
        self.background = background
        self.text_input = text_input
        self.surface = self.font.render(self.text_input, True, foreground, background)
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.surface, self.rect)

    def change_color(self, pos):
        x, y = pos
        new_bg = self.background
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            new_bg.a = 100
        else:
            new_bg.a = 20
        self.surface = self.font.render(self.text_input, True, self.foreground, new_bg)

class ContextMenu():

    def __init__(self, pos, font, text_input, foreground, background):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.foreground = foreground
        self.background = background
        self.text_input = text_input
        self.surface = self.font.render(self.text_input, True, foreground, background)
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.surface, self.rect)



########################################################
# Define our sprites
########################################################
class Player(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = LevelFunctions.load_image('Character.png', 1, (40, 40))
        self.rect.topleft = (x, y)
        self.pos = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2(0, 0)
        self.mask = pg.mask.from_surface(self.image)
        self.dead = False

    def respawn(self, pos):
        self.pos = pos.copy()
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.dead = False

    def update(self, dt, walls):
        self.velocity = pg.Vector2(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity.y -= 1
        if keys[pg.K_s]:
            self.velocity.y += 1
        if keys[pg.K_a]:
            self.velocity.x -= 1
        if keys[pg.K_d]:
            self.velocity.x += 1
        if self.velocity.length() > 1:
            self.velocity.normalize_ip()

        # Move X axis then resolve collisions
        self.pos.x += self.velocity.x * PLAYER_SPEED * dt / 1000
        self.rect.x = int(self.pos.x)
        for wall in pg.sprite.spritecollide(self, walls, False):
            if self.velocity.x > 0:
                self.rect.right = wall.rect.left
            elif self.velocity.x < 0:
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.x

        # Move Y axis then resolve collisions
        self.pos.y += self.velocity.y * PLAYER_SPEED * dt / 1000
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
        self.image, self.rect = LevelFunctions.load_image('coin.png', 1, (32, 32))
        self.rect.topleft = (x, y)
        self.anchor_pos = pg.math.Vector2(x, y)
        self.pos = pg.math.Vector2(x, y)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x, self.anchor_pos.y + math.sin(t * 2.5) * 10)
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
        self.image, self.rect = LevelFunctions.load_image('enemy.png', 1, (32, 32))
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pg.Vector2(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def update(self, dt):
        t = pg.time.get_ticks() / 1000.0
        self.pos = pg.Vector2(self.anchor_pos.x + math.sin(t * 3) * 300, self.anchor_pos.y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))


class SinEnemy(Enemy):

    def __init__(self, x, y, frequency, amplitude, delay,dir):
        super().__init__(x, y)
        self.amplitude = amplitude
        self.delay = delay
        self.frequency = frequency
        self.dir = dir 

    def update(self, dt):
        t = pg.time.get_ticks() / 1000.0
        if(self.dir =='x'):
            self.pos = pg.Vector2(self.anchor_pos.x + math.sin((t - self.delay) * self.frequency) * self.amplitude, self.anchor_pos.y)
        elif(self.dir =='y'):
            self.pos = pg.Vector2(self.anchor_pos.x, self.anchor_pos.y+ math.sin((t - self.delay) * self.frequency) * self.amplitude)
        else:
            raise ValueError("Incorrect direction given (x or y)!")
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

def SetUpLevel(level):
    global rectsOnScreen
    if level not in LEVEL_CONFIGS:
        raise ValueError("NO LEVEL SELECTED")
    config = LEVEL_CONFIGS[level]
    tile_size = config['tile_size']
    listOfSafeAreaBoxes, rectsOnScreen = LevelFunctions.convertImageToScreen(screen, config['map'], tile_size)
    safeArea = LevelFunctions.getAreaOfBox(listOfSafeAreaBoxes)
    return LevelTransition(
        level,
        pg.Rect(
            safeArea[2].x * tile_size + LevelFunctions.ORIENTATION_OFFSET_X,
            safeArea[2].y * tile_size + LevelFunctions.ORIENTATION_OFFSET_Y,
            safeArea[0].x * tile_size,
            safeArea[0].y * tile_size
        ))

class LinearEnemy(Enemy):

    def __init__(self, x, y, frequency, amplitude, delay, dir):
        super().__init__(x, y)
        self.amplitude = amplitude
        self.delay = delay
        self.frequency = frequency
        self.dir = dir

    def update(self, dt):
        t = pg.time.get_ticks() / 1000.0
        progress = ((t - self.delay) * self.frequency) % 2.0
        if progress > 1.0:
            progress = 2.0 - progress
        offset = (progress * 2 - 1) * self.amplitude
        if self.dir == 'x':
            self.pos = pg.Vector2(self.anchor_pos.x + offset, self.anchor_pos.y)
        elif self.dir == 'y':
            self.pos = pg.Vector2(self.anchor_pos.x, self.anchor_pos.y + offset)
        else:
            raise ValueError("Incorrect direction given (x or y)!")
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))


class SquareEnemy(Enemy):

    def __init__(self, x, y, frequency, amplitude, delay, clockwise=True):
        super().__init__(x, y)
        self.amplitude = amplitude
        self.delay = delay
        self.frequency = frequency
        self.clockwise = clockwise

    def update(self, dt):
        t = pg.time.get_ticks() / 1000.0
        progress = ((t - self.delay) * self.frequency) % 4.0
        a = self.amplitude
        if self.clockwise:
            if progress < 1.0:
                x_offset = -a + progress * 2 * a
                y_offset = -a
            elif progress < 2.0:
                x_offset = a
                y_offset = -a + (progress - 1.0) * 2 * a
            elif progress < 3.0:
                x_offset = a - (progress - 2.0) * 2 * a
                y_offset = a
            else:
                x_offset = -a
                y_offset = a - (progress - 3.0) * 2 * a
        else:
            if progress < 1.0:
                x_offset = -a + progress * 2 * a
                y_offset = a
            elif progress < 2.0:
                x_offset = a
                y_offset = a - (progress - 1.0) * 2 * a
            elif progress < 3.0:
                x_offset = a - (progress - 2.0) * 2 * a
                y_offset = -a
            else:
                x_offset = -a
                y_offset = -a + (progress - 3.0) * 2 * a
        self.pos = pg.Vector2(self.anchor_pos.x + x_offset, self.anchor_pos.y + y_offset)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class CircleEnemy(Enemy):

    def __init__(self, x, y, radius, freq, start_degs, clockwise=True):
        
        # set the anchor in super call
        super().__init__(x, y)
        self.radius = radius
        self.freq = freq
        self.start_degs = start_degs
        self.clockwise = clockwise
        # reset the pos in the rest,
        # pos should default with respect to radius & delay
        # final movement vector retrieved from radius and delay should be added to anchor_pos to get starting pos

        self.direction = pg.Vector2(1,0)
        self.direction.rotate_rad_ip(
            math.radians(start_degs)
        )
        # find initial distance (given)
        self.pos = self.anchor_pos + (self.direction * self.radius)
        
        # at the end update the rect pos as well
        self.rect.topleft = self.pos

    def update(self, dt):
        #  rotations per second per degrees
        di = self.freq * (dt / 1000) * 360
        if (self.clockwise): di = -di
        
        self.direction.rotate_ip(di)
        self.pos = self.anchor_pos + (self.direction * self.radius)
    
        # have to rotate pos around the anchorpos
        self.rect.topleft = self.pos




        

        

########################################################
# Level configuration - single source of truth for all level data
########################################################
LEVEL_CONFIGS = {
    1: {
        'map': './assets/level1map.png',
        'tile_size': 60,
        'enemies': lambda cx, cy: [
            SinEnemy(cx - 25, cy + 45, 3, 270, 0, 'x'),
            SinEnemy(cx - 25, cy - 15, 3, 270, 1, 'x'),
            SinEnemy(cx - 25, cy - 75, 3, 270, 0, 'x'),
            SinEnemy(cx - 25, cy - 135, 3, 270, 1, 'x'),
        ],
        'coins': lambda cx, cy: [
            Coin(cx - 90, cy - 90),
            Coin(cx - 50, cy - 50),
        ],
    },
    2: {
        'map': './assets/level_two.png',
        'tile_size': 60,
        'enemies': lambda cx, cy: [
            CircleEnemy(cx, cy, 300, 0.25, 1),
            SinEnemy(cx + 135, cy - 125, 3, 190, 1, 'y'),
            SinEnemy(cx + 75, cy - 125, 3, 190, 0, 'y'),
            SinEnemy(cx + 15, cy - 125, 3, 190, 1, 'y'),
            SinEnemy(cx - 45, cy - 125, 3, 190, 0, 'y'),
            SinEnemy(cx - 105, cy - 125, 3, 190, 1, 'y'),
            SinEnemy(cx - 165, cy - 125, 3, 190, 0, 'y'),
            SinEnemy(cx - 235, cy - 125, 3, 190, 1, 'y'),
            SinEnemy(cx - 295, cy - 125, 3, 190, 0, 'y'),
            SinEnemy(cx - 355, cy - 125, 3, 190, 1, 'y'),
        ],
        'coins': lambda cx, cy: [
            Coin(cx - 90, cy - 90),
            Coin(cx - 50, cy - 50),
        ],
    },
    3: {
        'map': './assets/level_duck.png',
        'tile_size': 50,
        'enemies': lambda cx, cy: [],
        'coins': lambda cx, cy: [
            Coin(cx - 90, cy - 90),
            Coin(cx - 50, cy - 50),
        ],
    },
    4: {
        'map': './assets/level_four.png',
        'tile_size': 60,
        'enemies': lambda cx, cy: [
            SquareEnemy(cx - 75, cy + 30, 1.3, 90, delay, clockwise=True)
            for delay in [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
        ],
        'coins': lambda cx, cy: [
            Coin(cx - 90, cy - 90),
        ],
    },
    5: {
        'map': './assets/level_five.png',
        'tile_size': 60,
        'enemies': lambda cx, cy: [
            # Upper corridor patrol - blocks the path near spawn
            SquareEnemy(cx - 60, cy - 380, 1.0, 70, 0.0, clockwise=True),
            SquareEnemy(cx - 60, cy - 380, 1.0, 70, 1.0, clockwise=True),
            SquareEnemy(cx - 60, cy - 380, 1.0, 70, 2.0, clockwise=True),
            # Mid-maze patrol - around the internal wall obstacles
            SquareEnemy(cx - 180, cy - 230, 0.8, 55, 0.0, clockwise=False),
            SquareEnemy(cx - 180, cy - 230, 0.8, 55, 1.5, clockwise=False),
            # Lower corridor patrol - guards the exit
            SquareEnemy(cx + 10, cy + 60, 1.0, 80, 0.0, clockwise=True),
            SquareEnemy(cx + 10, cy + 60, 1.0, 80, 1.0, clockwise=True),
            SquareEnemy(cx + 10, cy + 60, 1.0, 80, 2.0, clockwise=True),
        ],
        'coins': lambda cx, cy: [
            Coin(cx - 150, cy - 150),
            Coin(cx + 30, cy - 50),
        ],
    },
}

MAX_LEVEL = len(LEVEL_CONFIGS)

safeRT = SetUpLevel(level)

########################################################
# Win Screen!
########################################################

def win_screen():
    global background
    font1 = get_font(180)
    font2 = get_font(60)
    while True:
        screen.blit(background, (0, 0))
        win_UI = UIRect(
            pos=(screen.get_width() / 2, screen.get_height() / 2),
            font=font1,
            text_input="You Win!",
            foreground=pg.Color(0, 0, 0),
            background=pg.Color(255, 255, 255, 50)
        )
        TotalDeathsUI = UIRect(
            pos=(screen.get_width() / 4, screen.get_height() / 4),
            font=font2,
            text_input=f'TOTAL DEATHS: {numDeaths}',
            foreground=pg.Color(0, 0, 0),
            background=pg.Color(255, 255, 255, 50)
        )
        
        win_UI.update(screen)
        TotalDeathsUI.update(screen)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                pg.quit()
                return False
            


def reset_level_state(coins, cx, cy):
    coins.empty()
    for coin in LEVEL_CONFIGS[level]['coins'](cx, cy):
        coins.add(coin)
########################################################
# Game loop
########################################################
cooldownTimer = 0

def game_loop():

    global listOfSafeAreaBoxes, currentLevelSafeArea,level,safeRT,numDeaths,cooldownTimer


    # Build level background and walls
    
    newBg = pg.Surface(screen.get_size()).convert()
    newBg.fill(pg.Color(177, 172, 255))


    black_tuples = [(color, rect) for color, rect in rectsOnScreen if color == LevelFunctions.BACKGROUND_BLACK]
    walls = list(map(lambda obj: Wall(obj[1]), black_tuples))
    allwalls = pg.sprite.Group(walls)




    screen.fill(LevelFunctions.BACKGROUND_COLOR)
    screen.blit(newBg, (0, 0))
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            return False
    # Spawn player at first safe area
    player = Player(screen.get_width() / 2, screen.get_height() / 2)
    player_spawn = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    for (color, rect) in rectsOnScreen:
        if color == LevelFunctions.SAFE_AREA_COLOR:
            player_spawn = pg.Vector2(rect.left, rect.top)
            player.pos = player_spawn.copy()
            player.rect.topleft = (int(player.pos.x), int(player.pos.y))
            break


    # Draw level tiles
    config = LEVEL_CONFIGS[level]
    for (color, rect) in rectsOnScreen:
        pg.draw.rect(newBg, color, rect)
    LevelFunctions.cut_walls(newBg, rectsOnScreen, config['tile_size'])

    # Create enemies
    enemies = pg.sprite.Group()
    cx, cy = screen.get_width() / 2, screen.get_height() / 2
    for enemy in config['enemies'](cx, cy):
        enemies.add(enemy)

    # Spawn coins
    coins = pg.sprite.Group()
    for coin in config['coins'](cx, cy):
        coins.add(coin)
    LevelFunctions.assert_correct_coin_count(coins, level)
    


    player_group = pg.sprite.Group((player))
    

    ##################### Main game loop #####################
    running = True
    dt = 0
    while running:
        dt = clock.tick(60)
        #cooldown timer for death counter and coin counter
        if cooldownTimer > 0:
            cooldownTimer -= dt/1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False

        keys = pg.key.get_pressed()
        if keys[pg.K_m]:
            return True  # back to menu

        screen.fill(LevelFunctions.BACKGROUND_COLOR)
        screen.blit(newBg, (0, 0))

        player.update(dt, allwalls)
        coins.update()

        
        enemies.update(dt)
        enemies.draw(screen)
       
        player_group.draw(screen)
        coins.draw(screen)

        # Draw coin counter
        display_coins = ContextMenu((cx - 400, cy - 300), get_font(25), f'Coins: {LevelFunctions.num_coins_left_in_level(coins, level)}/{LevelFunctions.level_coins(level)}',
                                     pg.Color(0,0,0), None)
        display_coins.update(screen)

        # Check enemy collisions
        for enemy in enemies:
            if pg.sprite.collide_mask(player, enemy) and cooldownTimer <= 0:
                numDeaths += 1
                cooldownTimer = 0.5 # small cooldown to prevent multiple deaths from one collision
                player.respawn(player_spawn)
                reset_level_state(coins, cx, cy)
                break
        
        cc = pg.sprite.spritecollideany(player, coins, pg.sprite.collide_mask)
        if cc:
            coins.remove(cc)
        
        #Check for Finish area collisions
        if(safeRT):
            # DEBUG: pg.draw.rect(newBg, pg.Color(255,255,0), safeRT.rect) # draws yellow rectangle
            if(safeRT.rect.colliderect(player.rect)and cooldownTimer <=0 and len(coins) == 0):
                level += 1
                print(f'Send to new level {level}!')
                cooldownTimer = 1.0 # cooldown to prevent immediate re-triggering of level transition

                if level > MAX_LEVEL:  # player wins after beating all levels
                    win_screen()
                    return False  # return out of game completely
                    
                safeRT = SetUpLevel(level)
                return game_loop()  # restart loop cleanly
        
        #blit the ui
        font = get_font(20)
        
        DeathCounterUI = UIRect(
            pos=((screen.get_width() / 2 )+300, (screen.get_height() / 2) + 300),
            font=font,
            text_input=f'Deaths: {numDeaths}',
            foreground=pg.Color(0, 0, 0),
            background=None
        )
        DeathCounterUI.update(screen)

        pg.display.flip()

    return False




########################################################
# Main menu
########################################################
def splash_screen():
    screen.blit(splash_img, (0, 0))
    pg.display.flip()
    start = pg.time.get_ticks()
    while pg.time.get_ticks() - start < splash_screen_time_seconds * 1000: # show splash for 3 seconds
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                return True
        clock.tick(60)
    return True


def main_menu():
    play_button_font = get_font(60)
    while True:

        menu_mouse_pos = pg.mouse.get_pos()

        play_button = Button(
            pos=(screen.get_width() / 2, screen.get_height() / 2 + 300),
            font=play_button_font,
            text_input="PLAY",
            foreground=pg.Color(0, 0, 0),
            background=pg.Color(255, 255, 255, 50)
        )

        play_button.change_color(menu_mouse_pos)
        play_button.update(screen)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(menu_mouse_pos):
                    if not game_loop(): # go to end screen if false is returned
                        background.fill(LevelFunctions.BACKGROUND_COLOR)
                        return
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                pg.quit()
                return


if splash_screen():
    main_menu()
