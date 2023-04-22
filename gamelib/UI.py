import pygame

from gamelib.config import *
from gamelib.loading import *

class UI:
    def __init__(self, camera):
        self.camera = camera
        
    def update(self, player, screen, enemy_group):
        self.life = pygame.Surface((int(player.health/player.health_max*SCREEN_SIZE[0]/4), int(SCREEN_SIZE[1]/30)))
        self.life.fill((255,0,0))
        
        self.mana = pygame.Surface((int(player.mana/player.mana_max*SCREEN_SIZE[0]/4), int(SCREEN_SIZE[1]/30)))
        self.mana.fill((0,0,255))

        for i in enemy_group:
            if i.rect.colliderect(self.camera):
                if i.health > 0:
                    life = pygame.Surface((i.health/i.health_max*i.image.get_width(), int(SCREEN_SIZE[1]/100)))
                    life.fill((255,0,0))
                    screen.blit(life, (i.rect.x-self.camera.rect.x, i.rect.y))

        life = FONT[1].render(str(player.health), 1, (255,255,255))
        mana = FONT[1].render(str(player.mana), 1, (255,255,255))
        
        screen.blit(life, (int(SCREEN_SIZE[0]/50), int(SCREEN_SIZE[1]/40)))
        screen.blit(mana, (int(SCREEN_SIZE[0]/50), int(SCREEN_SIZE[1]/15)))

        screen.blit(self.life, (int(SCREEN_SIZE[0]/20), int(SCREEN_SIZE[1]/30)))
        screen.blit(self.mana, (int(SCREEN_SIZE[0]/20), int(SCREEN_SIZE[1]/14)))
