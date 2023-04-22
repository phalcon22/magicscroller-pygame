import pygame, gamelib.main, sys, gamelib.game, gamelib.menu
from pygame.locals import *

from gamelib.data import *
from gamelib.config import *
from gamelib.loading import *

class Map:

    def __init__(self, screen):
        #LOAD SAVE
        set_save_folder()
        self.niveau = load_save()

        #JOYSTICK INIT
        self.no_controller = False
        try:
            self.controller = pygame.joystick.Joystick(0)
        except:
            self.no_controller = True

        if not self.no_controller:
            self.controller.init()

        self.mouse_old = pygame.mouse.get_pos()
        self.mouse_new = pygame.mouse.get_pos()
        self.reinit = False
        #
        
        self.screen = screen
        self.option = 0

        self.level = []
        for i in range(NB_LEVEL):
            self.level.append(MAPLEVEL[i])
            self.level[i] = pygame.transform.scale(self.level[i], (int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2)))
        
        self.level_width = self.level[0].get_width()
        self.level_height = self.level[0].get_height()

        self.zooming = 2

        self.clock = pygame.time.Clock()
        self.update()
        self.draw(self.screen)

    def draw(self, surface):
        self.screen.blit(TITLE, (0,0))
        surface.blit(self.level[self.option], (int(SCREEN_SIZE[0]/2-self.level_width/2),int(SCREEN_SIZE[1]/2-self.level_height/2)))

        if self.option < NB_LEVEL-1:
            surface.blit(self.level[self.option+1], (int(SCREEN_SIZE[0]-self.level_width/4),int(SCREEN_SIZE[1]/2-self.level_height/2)))
        if self.option > 0:
            surface.blit(self.level[self.option-1], (int(-3*self.level_width/4),int(SCREEN_SIZE[1]/2-self.level_height/2)))

    def transition(self, direction):
        CLICK_SOUND.play()
        x = (5*self.level_width/4)/LVL_TRANSITION
        if direction == "right":
            self.option += 1
            for i in range(LVL_TRANSITION):
                self.screen.blit(TITLE, (0,0))
                if self.option > 1:
                    self.screen.blit(self.level[self.option-2], (int((-8*self.level_width/4)+x*(LVL_TRANSITION-i)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                self.screen.blit(self.level[self.option-1], (int((-3*self.level_width/4)+x*(LVL_TRANSITION-i)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                self.screen.blit(self.level[self.option], (int((SCREEN_SIZE[0]/2-self.level_width/2)+x*(LVL_TRANSITION-i)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                if self.option < NB_LEVEL-1:
                    self.screen.blit(self.level[self.option+1], (int((SCREEN_SIZE[0]-self.level_width/4)+x*(LVL_TRANSITION-i)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                pygame.display.flip()
                
        if direction == "left":
            self.option -= 1
            for i in range(LVL_TRANSITION):
                self.screen.blit(TITLE, (0,0))
                if self.option > 0:
                    self.screen.blit(self.level[self.option-1], (int((-3*self.level_width/4)+x*(i-LVL_TRANSITION)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                self.screen.blit(self.level[self.option], (int((SCREEN_SIZE[0]/2-self.level_width/2)+x*(i-LVL_TRANSITION)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                self.screen.blit(self.level[self.option+1], (int((SCREEN_SIZE[0]-self.level_width/4)+x*(i-LVL_TRANSITION)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                if self.option < NB_LEVEL-2:
                    self.screen.blit(self.level[self.option+2], (int((SCREEN_SIZE[0]+self.level_width)+x*(i-LVL_TRANSITION)),int(SCREEN_SIZE[1]/2-self.level_height/2)))
                    
                pygame.display.flip()

    def update(self):
        while 1:
            self.clock.tick(FPS)
                    
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        if self.option + 1 <= (self.niveau):
                            self.transition("right")
                    if e.key == pygame.K_LEFT:
                        if self.option - 1 >= 0:
                            self.transition("left")
                    if e.key == pygame.K_RETURN:
                        self.zoom()

                if not self.no_controller:
                    if e.type == JOYBUTTONDOWN:
                        if BUTTON[e.button] == "CROSS":
                            self.zoom()
                        if BUTTON[e.button] == "CIRCLE":
                            return
                        
                    if e.type == JOYHATMOTION:
                        if e.value[0] == 1:
                            if self.option + 1 <= (self.niveau):
                                self.transition("right")
                        if e.value[0] == -1:
                            if self.option - 1 >= 0:
                                self.transition("left")

            self.draw(self.screen)
            pygame.display.flip()

    def zoom(self):
        while self.zooming > 1:
            self.zooming -= 0.02/(1920/SCREEN_SIZE[0])
            LEVEL = MAPLEVEL[self.option]
            LEVEL = pygame.transform.scale(LEVEL, (int(SCREEN_SIZE[0]/self.zooming), int(SCREEN_SIZE[1]/self.zooming)))
            x = LEVEL.get_width()
            y = LEVEL.get_height()
            self.screen.blit(LEVEL, (int(SCREEN_SIZE[0]/2-x/2),int(SCREEN_SIZE[1]/2-y/2)))
            pygame.display.flip()
        self.zooming = 2/(1920/SCREEN_SIZE[0])
        gamelib.game.Game(self.screen, self.option+1)
