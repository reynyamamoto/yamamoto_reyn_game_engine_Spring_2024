

# This file was created by: Reyn Yamamoto
# Appreciation to Chris Bradfield

import pygame as pg
from settings import *
import sys
from os import path
from random import choice
from random import randint

vec = pg.math.Vector2

SPRITESHEET = "theBell.png"
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image


# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image = game.player_img
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]   
        self.last_update = 0
        self.material = True
        self.jumping = False
        self.walking = False 
        self.current_frame = 0   
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.last_dash_time = 0
        self.speed = 300
        self.score = 0
        self.collide_with_walls_flag = True  # Flag for collision behavior
        self.is_dashing = False  # Flag for dash state
        self.dash_duration = 0.5  # Dash duration in seconds
        self.dash_timer = 0  # Timer for dash duration
        self.dash_cooldown = 3.0 #dash cooldown
        game.all_sprites.add(self)


    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_SPACE]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_dash_time >= 3000:
                print("trying to dash")
                self.start_dash
                self.last_dash_time = current_time

#modified by chatgpt then me
    def start_dash(self):
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown = 3.0
    def handle_movement(self):
        if self.is_dashing:
            self.handle_dash()
    def handle_dash(self):
        if self.is_dashing:
            # Move player during dash
            self.dash_timer -= self.game.dt
            if self.dash_timer <= 0:
                self.is_dashing = False  # End dash when duration is over
        else:
            self.rect.x += self.vx * self.game.dt
            self.collide_with_walls('x')
            self.rect.y += self.vy * self.game.dt
            self.collide_with_walls('y')


    def collide_with_walls(self, dir):
        if not self.is_dashing:
            # Regular collision detection when not dashing
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for wall in hits:
                    if self.vx > 0:
                        self.rect.right = wall.rect.left
                    elif self.vx < 0:
                        self.rect.left = wall.rect.right
                    self.vx = 0
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for wall in hits:
                    if self.vy > 0:
                        self.rect.bottom = wall.rect.top
                    elif self.vy < 0:
                        self.rect.top = wall.rect.bottom
                    self.vy = 0   

    def collide_with_perimeters(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.perimeters, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: 
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.perimeters, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for sprite in hits:
                #when player collides with enemy, game exits/player dies
                if str(hits[0].__class__.__name__) == "Enemy":
                    pg.quit()
                    sys.exit()
                #when player collides with coins, score increments
                elif str(hits[0].__class__.__name__) == "Coin":
                    self.score += 1
                #when player collides with spikes, game exits/player dies
                elif str(hits[0].__class__.__name__) == "Spike":
                    pg.quit()
                    sys.exit()

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32),

                                ]
        self.walking_frames = [
                                self.spritesheet.get_image(64,0, 32, 32),
                                self.spritesheet.get_image(96,0, 32, 32),
        ]
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def update(self):
        # self.rect.x = self.x
        # self.rect.y = self.y
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.enemy, True)
        self.collide_with_group(self.game.spike, True)
        self.collide_with_perimeters('x')
        self.collide_with_perimeters('y')
        #coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        #if coin_hits:
            #print("I got a coin")
        #self.rect.x = self.x * TILESIZE
        #self.rect.y = self.y * TILESIZE
        self.handle_dash()
        self.handle_movement()
        if self.dash_cooldown > 0:
            self.dash_cooldown -= self.game.dt

    

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0


class Perimeter(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.perimeters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED) 
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
        
# coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.coin_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#################
            
# enemy class
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 1300
        #speed of enemy
    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -5
        #enemy acceleration
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def collide_with_enemies(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            
#new spike class
class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spike
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spike_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        