# This file was created by: Reyn Yamamoto

#new stationary enemy class, damage from enemy interaction, enemy movement

# goal of game to collect all coins before enemy can catch up to you while avoiding stationary spikes


'''
BETA Goal:
Dashing ability through wallsd
'''

# 
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# create a game class 
class Game: #capitalize classes; easier to identify
    # behold the methods...
    def __init__(self):
        pg.init()
        # adjusting width and height of screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # caption displayed on screen
        pg.display.set_caption("My First Video Game")
        # setting a clock for the game
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        #load game data
        self.load_data()
        self.score = 0

#importing image files
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.coin_img = pg.image.load(path.join(img_folder, 'coin.png')).convert_alpha()
        self.map_data = []
        self.player_img = pg.image.load(path.join(img_folder, 'player1.png')).convert_alpha()
        self.enemy_img = pg.image.load(path.join(img_folder, 'enemy.png')).convert_alpha()
        self.spike_img = pg.image.load(path.join(img_folder, 'spike.png')).convert_alpha()
    
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.spike = pg.sprite.Group()
        self.perimeters = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'e':
                    Enemy(self, col, row)
                if tile == 's':
                    Spike(self, col, row)
                if tile == 'w':
                    Perimeter(self, col, row)
    #run method, responsible for running the game engines
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # this is input
            self.events()
            # this is processing
            self.update()
            # this output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
            self.screen.fill(BGCOLOR)
            #self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player.score), 24, WHITE, WIDTH/2 - 32, 1)
            pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            # listening for events

                # keyboard events, arrow keys to move
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT:
                #         self.player.move(dx=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT:
                #         self.player.move(dx=1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP:
                #         self.player.move(dy=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN:
                #         self.player.move(dy=1)


    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
####################### Instantiate game... ###################

g = Game()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()