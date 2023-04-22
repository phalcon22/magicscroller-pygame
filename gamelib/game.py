import pygame, sys, gamelib.main

from gamelib.data import *
from gamelib.camera import *
from gamelib.level import *
from gamelib.menu.main_menu import *
from gamelib.menu.skills import *
from gamelib.menu.pause import *
from gamelib.menu.game_over import *
from gamelib.config import *
from gamelib.levels.level1 import *
from gamelib.UI import *

class Game:

    def __init__(self, screen, niveau):

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
        

        #MUSIC INIT
        pygame.mixer.music.load("data/musics/" + str(niveau) + ".ogg")
        pygame.mixer.music.play(-1)

        #GAME INIT
        self.niveau = niveau
        self.screen = screen
        self.level = Level(str(niveau), self.screen)
        self.player = self.level.player
        self.camera = Camera(self.screen, self.player, self.level.get_size()[0], self.level.get_size()[1])
        self.background = Background(niveau, screen, self.camera)
        self.UI = UI(self.camera)
        self.up = self.left = self.right = self.attack = False
        self.clock = pygame.time.Clock()

        if niveau == 1:
            self.level_script = Level1()
            
        self.update_game()

    def update_game(self):
        
        try:
            pygame.mixer.music.unpause()
        except:
            pass
        
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                    
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.up = self.left = self.right = self.attack = False
                    pygame.image.save(self.screen,"data/screenshot.jpg")
                    Pause(self.screen, self)
                        
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.player.jump(self.level.all_sprite)
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.player.protection(self.level)
                if event.type == KEYDOWN and event.key == K_LEFT:
                    self.left = True
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    self.right = True
                if event.type == KEYDOWN and event.key == K_RCTRL:
                    self.attack = True
                if event.type == KEYDOWN and event.key == K_LCTRL:
                    self.player.super_attack()

                if event.type == KEYUP and event.key == K_LEFT:
                    self.left = False
                if event.type == KEYUP and event.key == K_RIGHT:
                    self.right = False
                if event.type == KEYUP and event.key == K_RCTRL:
                    self.attack = False

                if not self.no_controller:
                    if event.type == JOYBUTTONDOWN:
                        if BUTTON[event.button] == "OPTIONS":
                            self.up = self.left = self.right = self.attack = False
                            pygame.image.save(self.screen,"data/screenshot.jpg")
                            Pause(self.screen, self)
                                
                        if BUTTON[event.button] == "CROSS":
                            self.player.jump(self.level.all_sprite)
                        if BUTTON[event.button] == "SQUARE":
                            self.attack = True

                    if event.type == JOYBUTTONUP:
                        if BUTTON[event.button] == "SQUARE":
                            self.attack = False

                    if event.type == JOYHATMOTION:
                        if event.value[0] == -1:
                            self.right = False
                            self.left = True
                        if event.value[0] == 1:
                            self.left = False
                            self.right = True
                        if event.value[0] == 0:
                            self.left = False
                            self.right = False

            if self.niveau == 1:
                self.level_script.update(self.screen, self.player, self)
                
            self.player.update(self.up, self.left, self.right, self.attack, self.level, self.camera)
            self.level.update(self.level.all_sprite, self.camera)
            self.background.update(self.camera)
            self.camera.update(self.level.all_sprite, self)
            self.camera.draw_sprites(self.screen, self.level.all_sprite)
            self.camera.draw_player(self.screen)
            self.UI.update(self.player, self.screen, self.level.enemy_group)

            fps = FONT[1].render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
            self.screen.blit(fps, (0,0))
            
            pygame.display.flip()

            if self.player.game_over:
                Game_over(self.screen, self.niveau)

            if self.player.win:
                self.continuer()

            self.clock.tick(FPS)

    def continuer(self):
        self.up = self.left = self.right = self.attack = False
        
        save_player(self.player)
        niveau = load_save()
        self.niveau += 1

        if self.niveau > niveau and self.niveau < NB_LEVEL:
            save(self.niveau)

        if self.niveau < NB_LEVEL:
            self.__init__(self.screen, self.niveau)
        if self.niveau == NB_LEVEL:
            Main_menu(self.screen)
