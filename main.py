# This file was created by: Ryan McElroy
# Code is based off of myGame_cozort
# https://github.com/kidscancode/pygame_tutorials/tree/master/platform 

# GameDesignGoals:
# add coin class
# Mobs that follow you
# Short jump with w tap
# go off one side, arive on other side

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
from math import floor
import math
import time

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.cd = Cooldown()
    
    def new(self):
        # add coin sound here
        self.coin_sound = pg.mixer.Sound(os.path.join(snd_folder, 'coin.mp3'))
        self.bgimage = pg.image.load(os.path.join(img_folder, "clouds.jpg")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self, pg.K_a, pg.K_d, pg.K_w, "theBell.png", 300,  300)
        self.player2 = Player(self,pg.K_j, pg.K_l, pg.K_i, "theBell.png", 300, 300)
        # add instances to groups
        self.all_sprites.add(self.player)
        
        # self.all_sprites.add(self.player2)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        # this is where we create mobs
        for m in range(0,5):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        # this is where we create coins
        for c in range(0,5):
            c = Coin(self, randint(0, WIDTH), randint(0, HEIGHT), 20, 20, "normal")
            self.all_sprites.add(c)
            self.all_coins.add(c)

        
        self.run()
    #setting up clock
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        self.cd.ticking()

        # handling collision in main instead of the mob or player class in sprites file
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, True)
        if mhits:
            print('this MOB collision happening in main')
            self.player.health -= 100

        # handling collision in main instead of the coin or player class in sprites file
        chits = pg.sprite.spritecollide(self.player, self.all_coins, True)
        if chits:
            print('this COIN collision happening in main')
            # play coin when collide with coin
            self.coin_sound.play()
            c = 0
        if chits:
                c += 1
                if c == 5:
                    self.draw_text("Win!", 100, WHITE, 400, HEIGHT/2)

        # if len(self.all_mobs) < 1:
        #     print("we are out of mobs!")
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH: 
            self.player.pos.x = 0
        
        # move plats up in group as you reach a point on screen
        # if self.player.pos.y < WIDTH/4:
        #     for p in self.all_platforms:
        #         p.rect.y += 25
        #         self.ground.rect.y += 25

        # this is what prevents the player from falling through the platform when falling down...
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        if hits:
            if hits[0].category == "moving":
                self.player.vel.x = hits[0].vel.x
            if self.player.vel.y > 0:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                print(self.player.vel.y)
                print(self.player.acc.y)
            elif self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y
            
        # checks to see if player collides specifically with the ground and sets him on top of it
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if ghits:
            self.player.pos.y = self.ground.rect.top
            self.player.vel.y = 0
            if self.player.cd.delta == 2:
                print(self.player.cd.delta)
                self.player.cd.event_reset()
                self.player.health -= 1

        hits = pg.sprite.spritecollide(self.player2, self.all_platforms, False)
        if hits:
            if self.player2.vel.y > 0:
                self.player2.pos.y = hits[0].rect.top
                self.player2.vel.y = 0
        # prevent player from jumping through bottom of plat in future update...
        ghits = pg.sprite.collide_rect(self.player2, self.ground)
        if ghits:
            self.player2.pos.y = self.ground.rect.top
            self.player2.vel.y = 0

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            self.cd.event_reset()
    #################### Draw #############################
    def draw(self):
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("P1 - Health: " + str(self.player.health), 22, WHITE, WIDTH/2, HEIGHT/24)
        # self.draw_text("P2 - Health: " + str(self.player2.health), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("acc: " + str(round(self.player.acc.y, 2)), 22, WHITE, 100, HEIGHT/6)
        self.draw_text("vel: " + str(round(self.player.vel.y, 2)), 22, WHITE, 100, HEIGHT/4)
        self.draw_text("cooldown: " + str(self.cd.delta), 22, WHITE, 200, HEIGHT/4)
        # you lose if you run out of health
        if self.player.health == 0:
            self.draw_text("You lose!", 100, WHITE, 400, HEIGHT/2)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()
