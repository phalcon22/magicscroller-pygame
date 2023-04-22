import pygame, sys, gamelib.main
from pygame.locals import *

from gamelib.loading import *
from gamelib.config import *
from gamelib.menu.main_menu import *

def cutscene(screen, text):
    font = FONT[1]
    alpha = 0
    intro = True
    outro = False
    height = len(text)*(font.get_height()+3)
    image = pygame.Surface((SCREEN_SIZE[0], height))
    y = 0
    for line in text:
        ren = font.render(line, 1, (255, 255, 255))
        image.blit(ren, (SCREEN_SIZE[0]/2-ren.get_width()/2, y*(font.get_height()+3)))
        y += 1

    #JOYSTICK INIT
    no_controller = False

    try:
        controller = pygame.joystick.Joystick(0)
    except:
        no_controller = True

    if not no_controller:
        controller.init()
        
    while 1:
        pygame.time.wait(10)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in (K_SPACE, K_RETURN, K_SPACE):
                    intro = False
                    outro = True
            if e.type == pygame.JOYBUTTONDOWN:
                intro = False
                outro = True 
                    
        if intro:
            if alpha < 255:
                alpha += 5
        if outro:
            if alpha > 0:
                alpha -= 5
            else:
                return
        image.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image, (0, SCREEN_SIZE[1]/2-image.get_height()/2))
        ren = font.render("Press a Button/Key to continue", 1, (255, 255, 255))
        screen.blit(ren, (SCREEN_SIZE[0]/2-ren.get_width()/2, 900/(1920/SCREEN_SIZE[0])))
        pygame.display.flip()

def tuto(screen, text):
    font = FONT[1]
    alpha = 0
    intro = True
    outro = False
    height = len(text)*(font.get_height()+3)
    pygame.image.save(screen, "data/tuto.jpg")
    game = pygame.image.load("data/tuto.jpg").convert()
    image = pygame.image.load("data/tuto.jpg").convert()
    area = pygame.Surface((SCREEN_SIZE[0]/2, (len(text)+4)*font.get_height()))
    area.fill((145,145,145))
    image.blit(area, (SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/4))
    y = 1
    for line in text:
        ren = font.render(line, 1, (255, 255, 255))
        image.blit(ren, (SCREEN_SIZE[0]/2-ren.get_width()/2, y*font.get_height()+(SCREEN_SIZE[1]/4)))
        y += 1
    y += 2

    #JOYSTICK INIT
    no_controller = False

    try:
        controller = pygame.joystick.Joystick(0)
    except:
        no_controller = True

    if not no_controller:
        controller.init()
        
    while 1:
        pygame.time.wait(10)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in (K_SPACE, K_RETURN, K_SPACE):
                    intro = False
                    outro = True
            if e.type == pygame.JOYBUTTONDOWN:
                intro = False
                outro = True 
                    
        if intro:
            if alpha < 200:
                alpha += 5
        if outro:
            if alpha > 0:
                alpha -= 5
            else:
                return
        image.set_alpha(alpha)
        screen.blit(game, (0, 0))
        screen.blit(image, (0, 0))
        ren = font.render("Press a Button/Key to continue", 1, (255, 255, 255))
        if alpha == 200:
            screen.blit(ren, (SCREEN_SIZE[0]/2-ren.get_width()/2, y*font.get_height()+(SCREEN_SIZE[1]/4)))
        pygame.display.flip()
