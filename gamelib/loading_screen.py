import pygame
from pygame.locals import *
from gamelib.config import *

TITLE = pygame.image.load("data/Title.png").convert()
TITLE = pygame.transform.scale(TITLE, SCREEN_SIZE)

FONT = pygame.font.Font(("data/fonts/font.ttf"), int(70/(1920/SCREEN_SIZE[0])))

ren = FONT.render("LOADING...", 1, (255,255,255))

def load_screen(screen, x):
    load = pygame.Surface((int(x*SCREEN_SIZE[0]/50), int(1*SCREEN_SIZE[1]/53)))
    load.fill((255,255,255))
    screen.blit(TITLE, (0,0))
    screen.blit(load, (0,0))
    screen.blit(ren, (int((SCREEN_SIZE[0]/2)-(ren.get_width()/2)),int((SCREEN_SIZE[1]/2)-(ren.get_height()/2))))
    pygame.display.flip()
