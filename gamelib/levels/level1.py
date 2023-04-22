import pygame

from gamelib.config import *
from gamelib.loading import *
from gamelib.cutscenes import*

def Controls(screen):
    tuto(screen, ["",
    "","","","","",
    "Move: Arrow Keys",
    "Jump: Space",
    "",
    ""])


class Level1:
    def __init__(self):
        self.controls = False
        self.attack = False
        self.protect = False

    def update(self, screen, player, game):
        if not self.controls and not player.chute_libre:
            self.controls = True
            game.left = game.up = game.right = game.attack = False
            tuto(screen, ["Move: Arrow Keys",
    "Jump: Space"])

        if not player.chute_libre and player.rect.x > SCREEN_SIZE[0] and not self.attack:
            self.attack = True
            game.left = game.up = game.right = game.attack = False
            tuto(screen, ["Attack: Right CTRL"])

        if not player.chute_libre and player.rect.x > 1.5*SCREEN_SIZE[0] and not self.protect:
            self.protect = True
            game.left = game.up = game.right = game.attack = False
            tuto(screen, ["Shield: RETURN"])
        
