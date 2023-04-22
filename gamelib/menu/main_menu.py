import pygame, gamelib.main, sys
from pygame.locals import *

from gamelib.data import *
from gamelib.config import *
from gamelib.loading import *
from gamelib.menu.map import *

class Main_menu:

    def __init__(self, screen):
        self.options = [["SELECT LEVEL", lambda: Map(screen)],
                        ["CONTROLS", lambda: gamelib.main.Controls(screen)],
                        ["QUIT GAME", sys.exit]]

        self.screen = screen
        self.font = FONT[1]
        self.old_option = 0
        self.option = 0
        self.width = 1
        self.color = [255, 255, 255]
        self.height = len(self.options)*self.font.get_height()

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

        #MOUSE INIT
        self.buttonx = []
        self.buttony = []
        self.out = False

        self.mouse = CURSOR
        self.mouse_rect = pygame.mouse.get_pos()

        #TEXT INIT        
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

        self.x = SCREEN_SIZE[0]/2-(self.width/2)
        self.y = SCREEN_SIZE[1]/2-(self.height/2)

        self.selected = pygame.Surface((self.width*2, self.font.get_height()))
        self.selected.fill((145,145,145))
        self.alpha = 20

        self.clock = pygame.time.Clock()
        
        if self.no_controller:
            self.draw(self.screen)
            self.update()
        if not self.no_controller:
            self.draw_joy(self.screen)
            self.update_joy()
        

    def draw(self, surface):

        surface.blit(TITLE, (0,0))
        
        i=0
        for o in self.options:
            if i==self.option and not self.out:
                if self.alpha < 130:
                    self.alpha += 10
                    self.selected.set_alpha(self.alpha)
                surface.blit(self.selected, (self.x-self.width/2, self.y + i*(self.font.get_height()+4)))
            text = o[0]
            ren = self.font.render(text, 1, self.color)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.font.get_height()+4)))
            self.buttonx.append(int((self.x+self.width/2) - ren.get_width()/2))
            self.buttony.append(int(self.y + i*(self.font.get_height()+4)))
            i+=1

        surface.blit(self.mouse, self.mouse_rect)
            
    def update(self):
        while 1:
            self.clock.tick(FPS)
            self.mouse_rect = pygame.mouse.get_pos()
            
            self.out = True
            contact = False
            for i in range(len(self.options)):
                if self.mouse_rect[0] > self.buttonx[i] - self.width/2 and self.mouse_rect[0] < self.buttonx[i] - self.width/2 + self.width*2:
                    if self.mouse_rect[1] > self.buttony[i] and self.mouse_rect[1] < self.buttony[i] + self.font.get_height():
                        contact = True
                        if self.old_option != self.option:
                            MENU_SOUND.play()
                        self.old_option = self.option
                        self.option = i
                        self.out = False
            if not contact:
                self.old_option = -1
            
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()

                if e.type == MOUSEBUTTONDOWN and not self.out:
                    if e.button == 1:
                        CLICK_SOUND.play()
                        self.options[self.option][1]()

                if not self.no_controller:
                    if e.type == JOYHATMOTION or e.type == JOYBUTTONDOWN:
                        self.update_joy()
                    if e.type == JOYAXISMOTION:
                        if abs(e.value) > 0.4:
                            self.update_joy()
                        
            if self.option > len(self.options)-1:
                self.option = 0
            if self.option < 0:
                self.option = len(self.options)-1

            self.draw(self.screen)
            pygame.display.flip()
            
    def draw_joy(self, surface):

        surface.blit(TITLE, (0,0))
        
        i=0
        for o in self.options:
            if i==self.option:
                if self.alpha < 130:
                    self.alpha += 10
                    self.selected.set_alpha(self.alpha)
                surface.blit(self.selected, (self.x-self.width/2, self.y + i*(self.font.get_height()+4)))
            text = o[0]
            ren = self.font.render(text, 1, self.color)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.font.get_height()+4)))
            self.buttonx.append(int((self.x+self.width/2) - ren.get_width()/2))
            self.buttony.append(int(self.y + i*(self.font.get_height()+4)))
            i+=1
            
    def update_joy(self):

        while 1:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()

                if e.type == JOYBUTTONDOWN:
                    if BUTTON[e.button] == "CROSS":
                        self.options[self.option][1]()

                if e.type == JOYHATMOTION:
                    if e.value[1] == 1:
                        self.option -= 1
                        MENU_SOUND.play()
                    if e.value[1] == -1:
                        self.option += 1
                        MENU_SOUND.play()

                if e.type == JOYAXISMOTION:
                    axis1 = round(self.controller.get_axis(1), 1)
                    if self.reinit:
                        if axis1 > 0.4:
                            self.option += 1
                            self.reinit = False
                        if axis1 < -0.4:
                            self.option -= 1
                            self.reinit = False
                        
                    if abs(self.controller.get_axis(1)) < 0.05:
                        self.reinit = True

                        
            if self.option > len(self.options)-1:
                self.option = 0
            if self.option < 0:
                self.option = len(self.options)-1

            self.mouse_old = self.mouse_new
            self.mouse_new = pygame.mouse.get_pos()

            if abs(self.mouse_old[0] - self.mouse_new[0] + self.mouse_old[1] - self.mouse_new[1]) > 2:
                self.update()
            else:
                self.draw_joy(self.screen)
            pygame.display.flip()
