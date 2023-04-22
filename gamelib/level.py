import pygame
from pygame.locals import *

from gamelib.sprites import *
from gamelib.config import *
from gamelib.player import *
from gamelib.background import *
from gamelib.enemies import *

class Level:
    def __init__(self, niveau, screen):
        
        level = "level/level" + niveau
        self.all_sprite = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.spells_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.flasks_group = pygame.sprite.Group()
        self.niveau = []
        self.level = open(level, "r")
        self.create_level()

    def create_level(self):
        x = 0
        y = 0
        for l in self.level:
            self.niveau.append(l)

        for line in self.niveau:
            for pill in line:

                if pill == "P":
                    self.player = Player(x, y)
                    self.all_sprite.add(self.player)                    

                if pill == "X":
                    self.all_sprite.add(Block(x, y))

                if pill == "w":
                    self.all_sprite.add(Way(x, y))
                    
                if pill == "M":
                    self.platform.add(Platform(x,y, 1))
                    self.all_sprite.add(self.platform)

                if pill == "m":
                    self.platform.add(Platform(x,y, -1))
                    self.all_sprite.add(self.platform)

                if pill == "O":
                    self.enemy_group.add(Ork(x,y))
                    self.all_sprite.add(self.enemy_group)

                if pill == "T":
                    self.enemy_group.add(Troll(x,y))
                    self.all_sprite.add(self.enemy_group)

                if pill == "W":
                    self.enemy_group.add(Warrior(x,y))
                    self.all_sprite.add(self.enemy_group)

                if pill == "E":
                    self.enemy_group.add(Elf(x,y, self.spells_group))
                    self.all_sprite.add(self.enemy_group)

                if pill == "l":
                    self.flasks_group.add(Flask(x,y, "life"))
                    self.all_sprite.add(self.flasks_group)
                    
                if pill == "e":
                    self.flasks_group.add(Flask(x,y, "mana"))
                    self.all_sprite.add(self.flasks_group)   

                x += BLOCK_SIZE
            y += BLOCK_SIZE
            x = 0

    def update(self, all_sprite, camera):
        self.platform.update()
        self.spells_group.update(camera)
        self.enemy_group.update(all_sprite, self.player, self.flasks_group)
        self.flasks_group.update(all_sprite)

    def get_size(self):
        lines = self.niveau
        line = max(lines, key=len)
        self.width = (len(line)-1)*BLOCK_SIZE
        self.height = (len(lines))*BLOCK_SIZE
        return (self.width, self.height)
