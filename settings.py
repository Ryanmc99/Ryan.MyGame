# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

from random import randint
# game settings 
WIDTH = 1000
HEIGHT = 800
FPS = 30

# player settings
PLAYER_JUMP = 8
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#placing all the platforms and catagorizing them
GROUND = (0, HEIGHT - 0, WIDTH, 40, "normal", (255, 255, 0))
PLATFORM_LIST = [
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal", (randint(0,255), randint(0,255), randint(0,255))),
                 (125, HEIGHT - 350, 100, 20, "moving", (255, 255, 255)),
                 (600, 500, 150, 20, "normal", (255, 255, 255)),
                 (350, 350, 100, 20, "normal", (255, 255, 255)),
                 (175, 600, 50, 20, "normal", (255, 255, 255)),
                 (800, 200, 170, 20, "normal", (255, 255, 255)),
                 (850, 600, 170, 20, "normal", (255, 255, 255)),
                 (50, 400, 170, 20, "normal", (255, 255, 255))]