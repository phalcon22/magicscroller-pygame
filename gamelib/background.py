import pygame
from random import *

from gamelib.config import *
from gamelib.loading import *

class Background:
    def __init__(self, niveau, screen, camera):
        self.screen = screen
        self.niveau = int(niveau)
        self.background_group = pygame.sprite.Group()

        #BACKGROUND LEVEL_1
        if self.niveau == 1:
            self.background_group.add(Static_landscape(screen, camera, LEVEL1[6]))
            self.background_group.add(Static_landscape(screen, camera, LEVEL1[0]))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[1], 5))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[1], 5, camera.rect.width))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[4], 4))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[4], 4, camera.rect.width))
            
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL1[2], 3, 0, 0.5))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL1[2], 3, camera.rect.width, 0.5))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[5], 2))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL1[5], 2, camera.rect.width))
            
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL1[3], 1.5, 0, 1))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL1[3], 1.5, camera.rect.width, 1))

        #BACKGROUND LEVEL_2
        if self.niveau == 2:
            self.background_group.add(Static_landscape(screen, camera, LEVEL2[8]))
            self.background_group.add(Static_landscape(screen, camera, LEVEL2[1]))
            self.background_group.add(Static_landscape(screen, camera, LEVEL2[7]))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[2], 5))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[2], 5, camera.rect.width))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[6], 4))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[6], 4, camera.rect.width))
            
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL2[3], 3, 0, 0.5))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL2[3], 3, camera.rect.width, 0.5))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[5], 2))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[5], 2, camera.rect.width))

            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[4], 2))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL2[4], 2, camera.rect.width))            

        #BACKGROUND LEVEL_3
        if self.niveau == 3:
            self.background_group.add(Static_landscape(screen, camera, LEVEL3[7]))
            self.background_group.add(Static_landscape(screen, camera, LEVEL3[0]))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[6], 5))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[6], 5, camera.rect.width))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[2], 4))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[2], 4, camera.rect.width))
            
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL3[1], 3, 0, 0.5))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL3[1], 3, camera.rect.width, 0.5))
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[3], 2))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[3], 2, camera.rect.width))

            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[4], 1.5))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[4], 1.5, camera.rect.width))

            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[5], 1))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL3[5], 1, camera.rect.width))

        #BACKGROUND LEVEL_4
        if self.niveau == 4:
            self.background_group.add(Static_landscape(screen, camera, LEVEL4[4]))

            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL4[0], 6, 0, 0.1))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL4[0], 6, camera.rect.width, 0.1))          

            self.background_group.add(Relative_landscape(screen, camera, LEVEL4[3], 4))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL4[3], 4, camera.rect.width))

            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL4[1], 3, 0, 0.1))
            self.background_group.add(Relative_dynamic_landscape(screen, camera, LEVEL4[1], 3, camera.rect.width, 0.1))  
            
            self.background_group.add(Relative_landscape(screen, camera, LEVEL4[2], 2))
            self.background_group.add(Relative_landscape(screen, camera, LEVEL4[2], 2, camera.rect.width))
    
        
    def update(self, camera):
        self.background_group.update(self.screen, camera)


class Static_landscape(pygame.sprite.Sprite):
    def __init__(self, screen, camera, landscape):
        pygame.sprite.Sprite.__init__(self)
        self.landscape = landscape
    def update(self, screen, camera):
        screen.blit(self.landscape, (0, 0))

class Relative_landscape(pygame.sprite.Sprite):
    def __init__(self, screen, camera, landscape, parallax, x=0):
        pygame.sprite.Sprite.__init__(self)
        self.landscape = landscape
        self.parallax = parallax
        self.x = x
    def update(self, screen, camera):
        screen.blit(self.landscape, (self.x-(camera.rect.x/self.parallax), 0))
        if self.x-(camera.rect.x/self.parallax)+SCREEN_SIZE[0] < 0:
            self.x += SCREEN_SIZE[0]*2
        if self.x-(camera.rect.x/self.parallax) > SCREEN_SIZE[0]:
            self.x -= SCREEN_SIZE[0]*2
        

class Relative_dynamic_landscape(pygame.sprite.Sprite):
    def __init__(self, screen, camera, landscape, parallax, x, relative=0):
        pygame.sprite.Sprite.__init__(self)
        self.landscape = landscape
        self.parallax = parallax
        self.x = x
        self.relative = relative/(1920/SCREEN_SIZE[0])
    def update(self, screen, camera):
        self.x -= self.relative
        screen.blit(self.landscape, (self.x-(camera.rect.x/self.parallax), 0))
        if self.x-(camera.rect.x/self.parallax)+SCREEN_SIZE[0] < 0:
            self.x += SCREEN_SIZE[0]*2
        if self.x-(camera.rect.x/self.parallax) > SCREEN_SIZE[0]:
            self.x -= SCREEN_SIZE[0]*2
        
