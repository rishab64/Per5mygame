# This file was created by: Rishab Manian

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint

# create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 20
        self.vx, self.vy = 0, 0
        self.coin_count = 0
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.vy -= self.speed
            print(self.vy)
        if keys[pg.K_LEFT]:
            self.vx -= self.speed
        if keys[pg.K_DOWN]:
            self.vy += self.speed
        if keys[pg.K_RIGHT]:
            self.vx += self.speed
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - TILESIZE
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
                
                print("Collided on x axis")
            else:
                print("not working...for hits")
        else:
            print("not working for dir check")

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 1
                print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x > WIDTH:
            self.x = 0
        elif self.rect.x < 0:
            self.x = WIDTH - TILESIZE

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')
        # teleport the player to the other side of the screen
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)


# added Mob - moving objects
# it is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 25

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        if self.rect.collide(self.game.player):
            self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


# Loading and modifying the sprites.py file for double jump and random item feature.
file_path_sprites = '/mnt/data/sprites.py'
file_path_main = '/mnt/data/main.py'

with open(file_path_sprites, 'r') as f:
    sprites_code = f.readlines()

with open(file_path_main, 'r') as f:
    main_code = f.readlines()

# Adding double jump capability and randomized sprite feature
updated_sprites_code = []
        # Double Jump Mechanism
if keys[pg.K_SPACE] or keys[pg.K_UP]:
    if self.jumps < 2:
        self.vy = -15  # Jump velocity
        self.jumps += 1

class RandomItem(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.type = 'powerup' if randint(0, 1) else 'debuff'
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 255, 0) if self.type == 'powerup' else (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def apply_effect(self, player):
        if self.type == 'powerup':
            player.speed += 5
        else:
            player.speed = max(5, player.speed - 5)  # Prevents speed below 5


for line in sprites_code:
    if "class Player(Sprite):" in line:
        updated_sprites_code.append(line)
        updated_sprites_code.append("        self.jumps = 0\n")
    elif "def update(self):" in line:
        updated_sprites_code.append("        self.jumps = 0 if self.collide_with_walls('y') else self.jumps\n")
        updated_sprites_code.append(line)
    elif "self.get_keys()" in line:
        updated_sprites_code.append(double_jump_logic)
    else:
        updated_sprites_code.append(line)

updated_sprites_code.append(random_item_logic)

# Saving the modified code
with open(file_path_sprites, 'w') as f:
    f.writelines(updated_sprites_code)

corrected_main_code = []

for line in main_code:
    if "from sprites_side_scroller import *" in line:
        corrected_main_code.append("from sprites import *\n")
    else:
        corrected_main_code.append(line)

# Saving the corrected main.py
file_path_main = '/mnt/data/main.py'
with open(file_path_main, 'w') as f:
    f.writelines(corrected_main_code)
