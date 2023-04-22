import pygame, gamelib.main, sys
from pygame.locals import *

from gamelib.data import *
from gamelib.config import *
from gamelib.loading import *

class Skills:
    def __init__(self, player, game, screen):
        
        self.player = player
        self.game = game
        self.screen = screen
        self.font = FONT[1]
        self.font16 = FONT[0]
        self.col = 0
        self.raw = self.player.skills[0]+1
        self.hcolor = (255, 0, 0)
        self.color = (255, 255, 255)

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

        self.bg = pygame.image.load("data/screenshot.jpg")
        self.skillpoints_text = self.font.render("Skill Points : ", 1, (0, 0, 0))

        self.unlock_list = [["","200","500"],["","200","500","1000","2000"],["","200","500","1000","2000"],["","200","500","1000","2000"],["","200","500","1000","2000"]]

        self.clock = pygame.time.Clock()
        self.update()
        self.draw(self.screen)
            
    def draw(self, surface):
        x = int(SCREEN_SIZE[0]/9)
        y = int(3*SCREEN_SIZE[1]/4)
        plus = 0

        surface.blit(self.bg,(0,0))

        surface.blit(self.skillpoints_text, (int(SCREEN_SIZE[0]/7),int(SCREEN_SIZE[1]/8)))
        surface.blit(self.skillpoints, (int(4*SCREEN_SIZE[0]/16),int(SCREEN_SIZE[1]/8)))

        
        for i in range(len(self.unlock_list)):
            for raw in range(len(self.unlock_list[i])):
                
                ren = self.font16.render(self.unlock_list[i][raw], 1, self.color)
                
                if raw == int(self.raw) and i == self.col:
                    surface.blit(CIRCLES[1], (x,y))
                    surface.blit(ren, (x+(35/(1920/SCREEN_SIZE[0])), y+(80/(1920/SCREEN_SIZE[0]))))
                else:
                    if raw <= self.player.skills[i]:
                        surface.blit(CIRCLES[2], (x,y))
                    else:
                        surface.blit(CIRCLES[0], (x,y))
                        surface.blit(ren, (x+(35/(1920/SCREEN_SIZE[0])), y+(80/(1920/SCREEN_SIZE[0]))))

                if i == 0 and raw < len(self.unlock_list[i]):
                    surface.blit(SPELLS[raw], (x+(5/(1920/SCREEN_SIZE[0])), y+(33/(1920/SCREEN_SIZE[0]))))

                if i == 1 and raw < len(self.unlock_list[i]):
                    surface.blit(SUPER_SPELL[self.player.skills[0]], (x+(22/(1920/SCREEN_SIZE[0])), y+(20/(1920/SCREEN_SIZE[0]))))         

                if i == 2 and raw < len(self.unlock_list[i]):
                    surface.blit(PROTECTION_SPELL, (x+(22/(1920/SCREEN_SIZE[0])), y+(20/(1920/SCREEN_SIZE[0]))))

                if i == 3 and raw < len(self.unlock_list[i]):
                    surface.blit(LIFE_POTION, (x+(31.5/(1920/SCREEN_SIZE[0])), y+(25/(1920/SCREEN_SIZE[0]))))

                if i == 4 and raw < len(self.unlock_list[i]):
                    surface.blit(MANA_POTION, (x+(31.5/(1920/SCREEN_SIZE[0])), y+(25/(1920/SCREEN_SIZE[0]))))
                
                for j in range(raw):
                    surface.blit(PLUS, (x+5+plus,y))
                    plus += 20

                y -= int(130/(1920/SCREEN_SIZE[0]))
                plus = 0
                
            x += int(SCREEN_SIZE[0]/5.5)
            y = int(3*SCREEN_SIZE[1]/4)
            
    def update(self):
        while 1:
            self.clock.tick(FPS)
            
            self.skillpoints = self.player.skillpoints
            self.skillpoints = self.font.render(str(self.skillpoints), 1, (0, 0, 0))
            
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        self.col -= 1
                    if e.key == pygame.K_RIGHT:
                        self.col += 1
                        
                    if e.key == pygame.K_RETURN:
                        if self.player.skills[self.col]+1 < len(self.unlock_list[self.col]):
                            if self.player.skillpoints >= int(self.unlock_list[self.col][self.raw]):
                                self.player.skills[self.col] += 1
                                self.player.skillpoints -= int(self.unlock_list[self.col][self.raw])
                                self.raw += 1

                if not self.no_controller:
                    if e.type == JOYBUTTONDOWN:
                        if BUTTON[e.button] == "CROSS":
                            if self.player.skills[self.col]+1 < len(self.unlock_list[self.col]):
                                if self.player.skillpoints >= int(self.unlock_list[self.col][self.raw]):
                                    self.player.skills[self.col] += 1
                                    self.player.skillpoints -= int(self.unlock_list[self.col][self.raw])
                                    self.raw += 1

                        if BUTTON[e.button] == "CIRCLE":
                            return

                    if e.type == JOYHATMOTION:
                        if e.value[0] == 1:
                            self.col += 1
                        if e.value[0] == -1:
                            self.col -= 1
                        
            if self.col >= len(self.unlock_list):
                self.col = 0
            if self.col < 0:
                self.col = len(self.unlock_list)-1

            self.raw = int(self.player.skills[self.col]+1)
            self.draw(self.screen)
            pygame.display.flip()
