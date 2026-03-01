import os
import pygame as pg
import math
import LevelFunctions

########################################################
# Define global variables
########################################################
level = 1
currentLevelSafeArea: tuple[pg.math.Vector2, pg.math.Vector2] = tuple[pg.math.Vector2(0,0),pg.math.Vector2(1,1)] 
listOfSafeAreaBoxes: list[pg.math.Vector2] = []
safeRectTransition = None
rectsOnScreen = []
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
pg.display.set_caption("Worlds Most Game")

screen.blit(background, (0, 0))
pg.display.flip()

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, "assets")


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



class Button():

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

    def change_color(self, pos):
        x, y = pos
        new_bg = self.background
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            new_bg.a = 100
        else:
            new_bg.a = 20
        self.surface = self.font.render(self.text_input, True, self.foreground, new_bg)


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
        self.image, self.rect = LevelFunctions.load_image('coin.png', 1, (32, 32))
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
        self.image, self.rect = LevelFunctions.load_image('enemy.png', 1, (32, 32))
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pg.Vector2(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def update(self):
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

    def update(self):
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
    match level:
        case 1:
            listOfSafeAreaBoxes, rectsOnScreen = LevelFunctions.convertImageToScreen(screen, './assets/level1map.png')
            safeArea = LevelFunctions.getAreaOfBox(listOfSafeAreaBoxes)
            safeRectTransition = LevelTransition(
                level,
                pg.Rect(
                    safeArea[2].x * LevelFunctions.BG_SQUARE_LENGTH + LevelFunctions.ORIENTATION_OFFSET_X,
                    safeArea[2].y * LevelFunctions.BG_SQUARE_LENGTH + LevelFunctions.ORIENTATION_OFFSET_Y,
                    safeArea[0].x * LevelFunctions.BG_SQUARE_LENGTH,
                    safeArea[0].y * LevelFunctions.BG_SQUARE_LENGTH
                ))
            return safeRectTransition
        case 2:
            listOfSafeAreaBoxes, rectsOnScreen = LevelFunctions.convertImageToScreen(screen, './assets/level_two.png')
            safeArea = LevelFunctions.getAreaOfBox(listOfSafeAreaBoxes)
            safeRectTransition = LevelTransition(
                level,
                pg.Rect(
                    safeArea[2].x * LevelFunctions.BG_SQUARE_LENGTH + LevelFunctions.ORIENTATION_OFFSET_X,
                    safeArea[2].y * LevelFunctions.BG_SQUARE_LENGTH + LevelFunctions.ORIENTATION_OFFSET_Y,
                    safeArea[0].x * LevelFunctions.BG_SQUARE_LENGTH,
                    safeArea[0].y * LevelFunctions.BG_SQUARE_LENGTH
                ))
            
            return safeRectTransition
        case 3:
            listOfSafeAreaBoxes, rectsOnScreen = LevelFunctions.convertImageToScreen(screen, './assets/level_duck.png', 50)
            smaller_bg_square_length = 50
            safeArea = LevelFunctions.getAreaOfBox(listOfSafeAreaBoxes)
            safeRectTransition = LevelTransition(
                level,
                pg.Rect(
                    safeArea[2].x * smaller_bg_square_length + LevelFunctions.ORIENTATION_OFFSET_X,
                    safeArea[2].y * smaller_bg_square_length + LevelFunctions.ORIENTATION_OFFSET_Y,
                    safeArea[0].x * smaller_bg_square_length,
                    safeArea[0].y * smaller_bg_square_length
                ))
            return safeRectTransition
        case _:
            raise ValueError("NO LEVEL SELECTED")
        
safeRT = SetUpLevel(level)
class LinearEnemy(Enemy):

    def __init__(self, x, y, frequency, amplitude, delay, dir):
        super().__init__(x, y)
        self.amplitude = amplitude
        self.delay = delay
        self.frequency = frequency
        self.dir = dir

    def update(self):
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

    def update(self):
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


########################################################
# Game loop
########################################################
happenOnce = True
def game_loop():
    global listOfSafeAreaBoxes, currentLevelSafeArea,happenOnce,level,safeRT
    dt = clock.tick(60) / 1000

    # Build level background and walls
    
    newBg = pg.Surface(screen.get_size()).convert()
    newBg.fill(pg.Color(177, 172, 255))


    black_tuples = [(color, rect) for color, rect in rectsOnScreen if color == LevelFunctions.BACKGROUND_BLACK]
    walls = list(map(lambda obj: Wall(obj[1]), black_tuples))
    allwalls = pg.sprite.Group(walls)

    # Spawn player at first safe area
    player = Player(screen.get_width() / 2, screen.get_height() / 2)
    player_spawn = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    for (color, rect) in rectsOnScreen:
        if color == LevelFunctions.SAFE_AREA_COLOR:
            player_spawn = pg.Vector2(rect.left, rect.top)
            player.pos = player_spawn.copy()
            player.rect.topleft = (int(player.pos.x), int(player.pos.y))
            #happenOnce = True
            break


    # Draw level tiles
    for (color, rect) in rectsOnScreen:
        pg.draw.rect(newBg, color, rect)
    match level:
        case 3:
            LevelFunctions.cut_walls(newBg, rectsOnScreen, 50)
        case _:
            LevelFunctions.cut_walls(newBg, rectsOnScreen)


    # Create enemies

    enemies = pg.sprite.Group()
    cx, cy = screen.get_width() / 2, screen.get_height() / 2
    match level:
        case 1:
            enemies.add(SinEnemy(cx - 25, cy + 45, 3, 270, 0,'x'))
            enemies.add(SinEnemy(cx - 25, cy - 15, 3, 270, 1,'x'))
            enemies.add(SinEnemy(cx - 25, cy - 75, 3, 270, 0,'x'))
            enemies.add(SinEnemy(cx - 25, cy - 135, 3, 270, 1,'x'))

        case 2:
            enemies.add(SinEnemy(cx - 25, cy - 135, 3, 270, 1,'x'))

        case 3:
            pass
        case _:
            raise ValueError("NO LEVEL SELECTED")
        

    # Spawn coin
    coin = Coin(cx, cy)
    allsprites = pg.sprite.Group((player, coin))

    # Main game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False

        keys = pg.key.get_pressed()
        if keys[pg.K_m]:
            return True  # back to menu

        if player.dead:
            player.respawn(player_spawn)

        screen.fill(LevelFunctions.BACKGROUND_COLOR)
        screen.blit(newBg, (0, 0))

        player.update(dt, allwalls)
        coin.update()

        
        enemies.update()
        enemies.draw(screen)
       
        allsprites.draw(screen)

        # Check enemy collisions
        for enemy in enemies:
            if pg.sprite.collide_mask(player, enemy):
                player.dead = True
                break

        #Check for Finish area collisions
        if(safeRT):
            # DEBUG: pg.draw.rect(newBg, pg.Color(255,255,0), safeRT.rect)
            if(safeRT.rect.colliderect(player.rect)and happenOnce ):
                level += 1
                print(f'Send to new level {level}!')
                safeRT = SetUpLevel(level)
                return game_loop()

        pg.display.flip()
        dt = clock.tick(60) / 1000

    return False


########################################################
# Main menu
########################################################
def main_menu():
    font = get_font(30)
    while True:
        screen.blit(background, (0, 0))
        menu_mouse_pos = pg.mouse.get_pos()

        play_button = Button(
            pos=(screen.get_width() / 2, screen.get_height() / 2),
            font=font,
            text_input="Play",
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
                    if not game_loop():
                        return
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                pg.quit()
                return


main_menu()

