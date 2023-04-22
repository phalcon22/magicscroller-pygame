import pygame
from pygame.locals import *

from gamelib.config import *
from gamelib.loading import *
        
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.nom= "platform"
        self.image = BLOCK
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.nom= "moving_platform"
        self.image = MOVING_PLATFORM
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.time = 180
        self.speed = speed/(1920/SCREEN_SIZE[0])

    def update(self):
        self.time -= 1
        if self.time < 0:
            self.speed = -self.speed
            self.time = 180
        self.x += self.speed
        self.rect.x = self.x

class Way(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.nom= "way"
        self.image = WAY
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Fireball(pygame.sprite.Sprite):
    def __init__(self, player):
        self.frame = 0
        pygame.sprite.Sprite.__init__(self)
        self.nom = "fireball"
        self.skill = player.skills[0]

        self.image = FIREBALL[self.skill][1][0]
        self.rect = self.image.get_rect()
        if player.direction == "right":
            self.rect.x = player.rect.right
        if player.direction == "left":
            self.rect.x = player.rect.left
            self.image = FIREBALL[self.skill][0][0]
        self.rect.y = player.rect.top
        self.direction = player.direction
        self.damages = 5 + player.skills[0]*2

    def update(self, camera):
        if not self.rect.colliderect(camera.rect):
            self.kill()
        
        if self.direction == "right":
            self.rect.x += (15/(1920/SCREEN_SIZE[0]))
        if self.direction == "left":
            self.rect.x -= (15/(1920/SCREEN_SIZE[0]))
        self.animation()

    def animation(self):
        if self.direction == "right":
            self.image = FIREBALL[self.skill][1][self.frame]
        if self.direction == "left":
            self.image = FIREBALL[self.skill][0][self.frame]
        self.frame += 1
        if self.frame > 5:
            self.frame = 0

class SuperFireball(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        self.frame = 0
        pygame.sprite.Sprite.__init__(self)
        self.nom = "fireball"
        self.skill = player.skills[0]

        self.image = SUPER[self.skill][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damages = 5 + player.skills[0]*2

    def update(self, camera):
        if not self.rect.colliderect(camera.rect):
            self.kill()
        
        self.rect.y += (15/(1920/SCREEN_SIZE[0]))
        self.animation()

    def animation(self):
        self.image = SUPER[self.skill][self.frame]
        self.frame += 1
        if self.frame > 5:
            self.frame = 0

class Protection(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.nom = "protection"
        
        self.image = PROTECTION
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x - (50/(1920/SCREEN_SIZE[0]))
        self.rect.y = self.player.rect.y - (50/(1920/SCREEN_SIZE[0]))
        self.time = 36 + 36*player.skills[2]

    def update(self, camera):
        self.rect.x = self.player.rect.x - (50/(1920/SCREEN_SIZE[0]))
        self.rect.y = self.player.rect.y - (50/(1920/SCREEN_SIZE[0]))
        if self.time > 0:
            self.time -= 1
        if self.time == 0:
            self.kill()
        
class Flask(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.nom = name
        if name == "mana":
            self.image = MANA_FLASK
        if name == "life":
            self.image = LIFE_FLASK
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.movy = 0
        self.contact = False

        self.initialized = False

    def update(self, all_sprite):
        if not self.initialized:
            self.collide(all_sprite)
            self.initialized = True
            
        if not self.contact:
            self.movy += 0.5
            self.rect.y += self.movy
            self.collide(all_sprite)

    def collide(self, all_sprite):
        for o in all_sprite:
            if self.rect.colliderect(o):
                if o.nom == "platform" or o.nom == "moving_platform" or o.nom ==   "way":
                    self.rect.bottom = o.rect.top
                    self.contact = True

class Arrow(pygame.sprite.Sprite):
    def __init__ (self, elf, all_sprite):
        self.frame = 0
        pygame.sprite.Sprite.__init__(self)
        self.elf = elf
        self.nom = "arrow"

        self.image = ARROW[0]
        self.rect = self.image.get_rect()
        if elf.direction == "right":
            self.rect.left = elf.rect.right
            self.image = ARROW[1]
        if elf.direction == "left":
            self.rect.right = elf.rect.left
            self.image = ARROW[0]
        self.rect.y = elf.rect.centery
        self.direction = elf.direction
        self.damages = 10
        self.all_sprite = all_sprite

    def update(self, camera):
        if not self.rect.colliderect(camera.rect):
            self.kill()
            
        if self.direction == "right":
            self.rect.x += 15/(1920/SCREEN_SIZE[0])
        if self.direction == "left":
            self.rect.x -= 15/(1920/SCREEN_SIZE[0])
            
        self.collide()

    def collide(self):
        for o in self.all_sprite:
            if self.rect.colliderect(o):
                if o.nom == "protection":
                    self.kill()
