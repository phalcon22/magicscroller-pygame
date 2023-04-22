import pygame
from pygame.locals import *

from gamelib.config import *

class Camera():
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.height = SCREEN_SIZE[1]
        self.rect.center = self.player.rect.center
        self.rect.centerx = self.player.rect.centerx + SCREEN_SIZE[0]/6
        self.world_rect = Rect(0, 0, level_width, SCREEN_SIZE[1])

        self.up_mode = False
        self.down_mode = False

        self.rect.clamp_ip(self.world_rect)

    #FOLLOW PLAYER
    def update (self, all_sprite, game):

        if self.player.rect.centerx + SCREEN_SIZE[0]/6 < self.rect.centerx:
            self.rect.centerx = self.player.rect.centerx + SCREEN_SIZE[0]/6
        if self.player.rect.centerx + SCREEN_SIZE[0]/6 > self.rect.centerx:
            self.rect.centerx = self.player.rect.centerx + SCREEN_SIZE[0]/6

        self.rect.clamp_ip(self.world_rect)

    #SHOW GAME
    def draw_sprites(self, screen, all_sprite):
        for s in all_sprite:
            if s.rect.colliderect(self.rect):
                if s.nom != "player" and s.nom != "troll":
                    screen.blit(s.image, (s.rect.x-self.rect.x, s.rect.y-self.rect.y))

                if s.nom == "troll":
                    if s.attack:
                        y = -190
                    if not s.attack:
                        y = -0
                    screen.blit(s.image, (s.rect.x-self.rect.x, s.rect.y-self.rect.y+y/(1920/SCREEN_SIZE[0])))

    #FIX PLAYER IMAGES POSITION
    def draw_player(self, screen):
        if not self.player.death_cooldown > 0:
            if self.player.hit_cooldown <= 95:
                if not self.player.attack_cooldown > 0:
                    if not self.player.jump_mode:
                        if self.player.movx == 0:
                            y = -80
                            if self.player.direction == "right":
                                x = -60
                            if self.player.direction == "left":
                                x = -85
                        if self.player.movx != 0:
                            y = -100
                            if self.player.direction == "right":
                                x = -65
                            if self.player.direction == "left":
                                x = -110
                    if self.player.jump_mode:
                        y = -95
                        if self.player.direction == "right":
                            x = -60
                        if self.player.direction == "left":
                            x = -95
                if self.player.attack_cooldown > 0:
                    y = -116
                    if self.player.direction == "right":
                        x = -67
                    if self.player.direction == "left":
                        x = -255
            if self.player.hit_cooldown > 95:
                y = -80
                if self.player.direction == "right":
                    x = -100
                if self.player.direction == "left":
                    x = -85
        if self.player.death_cooldown > 0:
            y = -76
            if self.player.direction == "right":
                x = -55
            if self.player.direction == "left":
                x = -80
                
        screen.blit(self.player.image, (self.player.rect.x-self.rect.x+(x/(1920/SCREEN_SIZE[0])), self.player.rect.y-self.rect.y+(y/(1920/SCREEN_SIZE[0]))))
