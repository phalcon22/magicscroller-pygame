import pygame

from random import randint
from gamelib.config import *
from gamelib.sprites import *
from gamelib.loading import *

class Ork(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #initialisation des attributs de l'Elfe
        pygame.sprite.Sprite.__init__(self)
        self.health_max = self.health = 1
        self.damages = 15
        self.points = 100
        self.nom = "ork"
        self.movx = 0
        self.movy = 0
        self.image = ORK[0][0][3][0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.level = 0
        self.attack = False
        self.death_cooldown = -1
        self.direction = "left"
        
        self.initialized = False

    def update(self, all_sprite, player, flask_group):
        #fonction mise à jour du Warrior
        if not self.initialized:
            self.collide(all_sprite, "y")
            self.initialized = True
        
        self.test_gameover(player, flask_group, all_sprite)
        self.pos_update(all_sprite, player)
        self.animation_update()

    def pos_update(self, all_sprite, player):
        #fonction qui le fait se déplacer le personnage en fonction de la position du joueur
        if self.death_cooldown == -1:
            self.x += self.movx
            self.rect.x = self.x
        self.collide(all_sprite, "x")

        self.movy += 1
        self.y += self.movy
        self.rect.y = self.y
        self.collide(all_sprite, "y")

        if self.death_cooldown == -1:
            if abs(player.rect.centery - self.rect.centery) < 100/(1920/SCREEN_SIZE[0]):
                if player.rect.centerx - self.rect.centerx < 0:
                    if player.rect.centerx - self.rect.centerx > -1600/(1920/SCREEN_SIZE[0]):
                        self.movx = -5/(1920/SCREEN_SIZE[0])
                        self.direction = "left"
                        
                if player.rect.centerx - self.rect.centerx > 0:
                    if player.rect.centerx - self.rect.centerx < 1200/(1920/SCREEN_SIZE[0]):
                        self.movx = 5/(1920/SCREEN_SIZE[0])
                        self.direction = "right"
                
                if abs(player.rect.centerx - self.rect.centerx) < 150/(1920/SCREEN_SIZE[0]):
                    self.movx = 0
                    self.attack = True
                else:
                    self.attack = False
                    
            if abs(player.rect.centery - self.rect.centery) >= 100/(1920/SCREEN_SIZE[0]) and not player.jump_mode:
                self.movx = 0
            if abs(player.rect.centerx - self.rect.centerx) > 1920/(1920/SCREEN_SIZE[0]):
                self.movx = 0
            
    def collide(self, all_sprite, orientation):
        #fonction collide qui détermine si les ennemis rentrent en contact avec une platforme ou une attaque
        self.chute_libre = True
        contact = False
        movy = self.movy
        for o in all_sprite:
            if self.rect.colliderect(o):

                if o.nom == "platform" or o.nom == "moving_platform" or o.nom == "protection" or o.nom == "way":
                
                    if orientation == "x":
                        if self.rect.centerx > o.rect.centerx:
                            self.rect.left = o.rect.right
                            self.x = self.rect.x
                        if self.rect.centerx < o.rect.centerx:
                            self.rect.right = o.rect.left
                            self.x = self.rect.x

                    if orientation == "y":
                        if self.movy > 0 or not self.initialized:
                            self.rect.bottom = o.rect.top
                            self.y = self.rect.y
                            self.movy = 0
                            contact = True
                            self.chute_libre = False
                            if o.nom == "moving_platform":
                                self.x += o.speed
                                self.rect.x = self.x
                        if self.movy < 0:
                            self.rect.top = o.rect.bottom
                            self.y = self.rect.y
                            self.movy = 0

                if o.nom == "way":
                    if orientation == "y":
                        if self.movy >= 0:
                            if self.rect.bottom < o.rect.bottom:
                                self.rect.bottom = o.rect.top
                                self.y = self.rect.y
                                self.movy = 0
                                contact = True
                                self.chute_libre = False

                if o.nom == "fireball" or o.nom == "arrow":
                    if self.death_cooldown == -1:
                        HIT_SOUND.play()
                        self.health -= o.damages
                        o.kill()
                            
        if not contact and orientation == "y":
            self.y -= self.movy
            self.movy -= 1
            self.movy += FALL
            self.y += self.movy
            self.rect.y = self.y
            
    def animation_update(self):
        #DETERMINE DIRECTION
        if self.direction == "right":
            direction = 1
        if self.direction == "left":
            direction = 0

        #DETERMINE STATE
        if not self.attack:
            if self.movx == 0:
                state = 3
            if self.movx != 0:
                state = 5
        if self.attack:
            state = 0

        if self.death_cooldown > 0:
            state = 1

        #DETERMINE FRAME
        self.frame += 1
        if self.frame >= ANIM_ROT: self.frame = 0

        if self.frame < ANIM_ROT/5:
            frame = 0
        elif self.frame < 2*ANIM_ROT/5:
            frame = 1
        elif self.frame < 3*ANIM_ROT/5:
            frame = 2
        elif self.frame < 4*ANIM_ROT/5:
            frame = 3
        elif self.frame < ANIM_ROT:
            frame = 4

        if self.death_cooldown > 72:
            frame = 0
        elif self.death_cooldown > 54:
            frame = 1
        elif self.death_cooldown > 36:
            frame = 2
        elif self.death_cooldown > 18:
            frame = 3
        elif self.death_cooldown >= 0:
            frame = 4
             
        self.image = ORK[self.level][direction][state][frame]

    def test_gameover(self, player, flask_group, all_sprite):         
        if self.health <= 0 and self.death_cooldown == -1:
            player.skillpoints += self.points
            self.death_cooldown = 90
            self.movx = 0

        if self.death_cooldown > 0:
            self.death_cooldown -= 1
        if self.death_cooldown == 0:
            self.drop(flask_group, all_sprite)

    def drop(self, flask_group, all_sprite):
        x = randint(0,10)
        if x <= 2:
            flask_group.add(Flask(self.x, self.y, "life"))
        if x >= 8:
            flask_group.add(Flask(self.x, self.y, "mana"))
        all_sprite.add(flask_group)
        self.kill()

class Warrior(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #initialisation des attributs de l'Elfe
        pygame.sprite.Sprite.__init__(self)
        self.health_max = self.health = 30
        self.damages = 15
        self.points = 100
        self.nom = "warrior"
        self.movx = 0
        self.movy = 0
        self.image = WARRIOR[0][0][3][0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.level = 0
        self.attack = False
        self.death_cooldown = -1
        self.direction = "left"
        
        self.initialized = False

    def update(self, all_sprite, player, flask_group):
        #fonction mise à jour du Warrior
        if not self.initialized:
            self.collide(all_sprite, "y")
            self.initialized = True
        
        self.test_gameover(player, flask_group, all_sprite)
        self.pos_update(all_sprite, player)
        self.animation_update()

    def pos_update(self, all_sprite, player):
        #fonction qui le fait se déplacer le personnage en fonction de la position du joueur
        if self.death_cooldown == -1:
            self.x += self.movx
            self.rect.x = self.x
        self.collide(all_sprite, "x")

        self.movy += 1
        self.y += self.movy
        self.rect.y = self.y
        self.collide(all_sprite, "y")

        if self.death_cooldown == -1:
            if abs(player.rect.centery - self.rect.centery) < 100/(1920/SCREEN_SIZE[0]):
                if player.rect.centerx - self.rect.centerx < 0:
                    if player.rect.centerx - self.rect.centerx > -1600/(1920/SCREEN_SIZE[0]):
                        self.movx = -5/(1920/SCREEN_SIZE[0])
                        self.direction = "left"
                        
                if player.rect.centerx - self.rect.centerx > 0:
                    if player.rect.centerx - self.rect.centerx < 1200/(1920/SCREEN_SIZE[0]):
                        self.movx = 5/(1920/SCREEN_SIZE[0])
                        self.direction = "right"
                
                if abs(player.rect.centerx - self.rect.centerx) < 150/(1920/SCREEN_SIZE[0]):
                    self.movx = 0
                    self.attack = True
                else:
                    self.attack = False
                    
            if abs(player.rect.centery - self.rect.centery) >= 100/(1920/SCREEN_SIZE[0]) and not player.jump_mode:
                self.movx = 0
            if abs(player.rect.centerx - self.rect.centerx) > 1920/(1920/SCREEN_SIZE[0]):
                self.movx = 0
            
    def collide(self, all_sprite, orientation):
        #fonction collide qui détermine si les ennemis rentrent en contact avec une platforme ou une attaque
        self.chute_libre = True
        contact = False
        movy = self.movy
        for o in all_sprite:
            if self.rect.colliderect(o):

                if o.nom == "platform" or o.nom == "moving_platform" or o.nom == "protection" or o.nom == "way":
                
                    if orientation == "x":
                        if self.rect.centerx > o.rect.centerx:
                            self.rect.left = o.rect.right
                            self.x = self.rect.x
                        if self.rect.centerx < o.rect.centerx:
                            self.rect.right = o.rect.left
                            self.x = self.rect.x

                    if orientation == "y":
                        if self.movy > 0 or not self.initialized:
                            self.rect.bottom = o.rect.top
                            self.y = self.rect.y
                            self.movy = 0
                            contact = True
                            self.chute_libre = False
                            if o.nom == "moving_platform":
                                self.x += o.speed
                                self.rect.x = self.x
                        if self.movy < 0:
                            self.rect.top = o.rect.bottom
                            self.y = self.rect.y
                            self.movy = 0

                if o.nom == "way":
                    if orientation == "y":
                        if self.movy >= 0:
                            if self.rect.bottom < o.rect.bottom:
                                self.rect.bottom = o.rect.top
                                self.y = self.rect.y
                                self.movy = 0
                                contact = True
                                self.chute_libre = False

                if o.nom == "fireball" or o.nom == "arrow":
                    if self.death_cooldown == -1:
                        HIT_SOUND.play()
                        self.health -= o.damages
                        o.kill()
                            
        if not contact and orientation == "y":
            self.y -= self.movy
            self.movy -= 1
            self.movy += FALL
            self.y += self.movy
            self.rect.y = self.y
            
    def animation_update(self):
        #DETERMINE DIRECTION
        if self.direction == "right":
            direction = 1
        if self.direction == "left":
            direction = 0

        #DETERMINE STATE
        if not self.attack:
            if self.movx == 0:
                state = 3
            if self.movx != 0:
                state = 5
        if self.attack:
            state = 0

        if self.death_cooldown > 0:
            state = 1

        #DETERMINE FRAME
        self.frame += 1
        if self.frame >= ANIM_ROT: self.frame = 0

        if self.frame < ANIM_ROT/5:
            frame = 0
        elif self.frame < 2*ANIM_ROT/5:
            frame = 1
        elif self.frame < 3*ANIM_ROT/5:
            frame = 2
        elif self.frame < 4*ANIM_ROT/5:
            frame = 3
        elif self.frame < ANIM_ROT:
            frame = 4

        if self.death_cooldown > 72:
            frame = 0
        elif self.death_cooldown > 54:
            frame = 1
        elif self.death_cooldown > 36:
            frame = 2
        elif self.death_cooldown > 18:
            frame = 3
        elif self.death_cooldown >= 0:
            frame = 4
             
        self.image = WARRIOR[self.level][direction][state][frame]

    def test_gameover(self, player, flask_group, all_sprite):         
        if self.health <= 0 and self.death_cooldown == -1:
            player.skillpoints += self.points
            self.death_cooldown = 90
            self.movx = 0

        if self.death_cooldown > 0:
            self.death_cooldown -= 1
        if self.death_cooldown == 0:
            self.drop(flask_group, all_sprite)

    def drop(self, flask_group, all_sprite):
        x = randint(0,10)
        if x <= 2:
            flask_group.add(Flask(self.x, self.y, "life"))
        if x >= 8:
            flask_group.add(Flask(self.x, self.y, "mana"))
        all_sprite.add(flask_group)
        self.kill()


class Elf(pygame.sprite.Sprite):
    def __init__(self, x, y, spells_group):
        pygame.sprite.Sprite.__init__(self)
        self.health_max = self.health = 10
        self.damages = 5
        self.points = 100
        self.nom = "elf"
        self.movx = 0
        self.movy = 0
        self.image = ELF[0][0][3][0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.level = 0
        self.attack = False
        self.attack_cooldown = 0
        self.death_cooldown = -1
        self.direction = "left"
        self.spells_group = spells_group

        self.initialized = False

    def update(self, all_sprite, player, flask_group):
        if not self.initialized:
            self.collide(all_sprite, "y")
            self.initialized = True
            
        self.test_gameover(player, flask_group, all_sprite)
        self.pos_update(all_sprite, player)
        self.animation_update()

    def pos_update(self, all_sprite, player):

        if self.death_cooldown == -1:
            self.x += self.movx
            self.rect.x = self.x
        self.collide(all_sprite, "x")

        self.movy += 1
        self.y += self.movy
        self.rect.y = self.y
        self.collide(all_sprite, "y")

        if self.death_cooldown == -1:
            if abs(player.rect.centery - self.rect.centery) < 100/(1920/SCREEN_SIZE[0]):
                if player.rect.centerx - self.rect.centerx < 0:
                    if player.rect.centerx - self.rect.centerx > -1600/(1920/SCREEN_SIZE[0]):
                        self.direction = "left"
                        
                if player.rect.centerx - self.rect.centerx > 0:
                    if player.rect.centerx - self.rect.centerx < 1000/(1920/SCREEN_SIZE[0]):
                        self.direction = "right"

            if self.attack_cooldown == 0:
                if abs(player.x - self.x)< 1500/(1920/SCREEN_SIZE[0]):
                    if abs(player.y - self.y)< 100/(1920/SCREEN_SIZE[0]):
                        self.attack_cooldown = 180
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            if self.attack_cooldown == 150:
                self.spells_group.add(Arrow(self, all_sprite))
                all_sprite.add(self.spells_group)      
        
        
            
    def collide(self, all_sprite, orientation):
        self.chute_libre = True
        contact = False
        movy = self.movy
        for o in all_sprite:
            if self.rect.colliderect(o):

                if o.nom == "platform" or o.nom == "moving_platform" or o.nom == "protection" or o.nom == "way":
                
                    if orientation == "x":
                        if self.rect.centerx > o.rect.centerx:
                            self.rect.left = o.rect.right
                            self.x = self.rect.x
                        if self.rect.centerx < o.rect.centerx:
                            self.rect.right = o.rect.left
                            self.x = self.rect.x

                    if orientation == "y":
                        if self.movy > 0 or not self.initialized:
                            self.rect.bottom = o.rect.top
                            self.y = self.rect.y
                            self.movy = 0
                            contact = True
                            self.chute_libre = False
                            if o.nom == "moving_platform":
                                self.x += o.speed
                                self.rect.x = self.x
                        if self.movy < 0:
                            self.rect.top = o.rect.bottom
                            self.y = self.rect.y
                            self.movy = 0

                if o.nom == "way":
                    if orientation == "y":
                        if self.movy >= 0:
                            if self.rect.bottom < o.rect.bottom:
                                self.rect.bottom = o.rect.top
                                self.y = self.rect.y
                                self.movy = 0
                                contact = True
                                self.chute_libre = False

                if o.nom == "fireball" or o.nom == "arrow":
                    if self.death_cooldown == -1:
                        HIT_SOUND.play()
                        self.health -= o.damages
                        o.kill()
                            
        if not contact and orientation == "y":
            self.y -= self.movy
            self.movy -= 1
            self.movy += FALL
            self.y += self.movy
            self.rect.y = self.y
            
    def animation_update(self):
        #DETERMINE DIRECTION
        if self.direction == "right":
            direction = 1
        if self.direction == "left":
            direction = 0

        #DETERMINE STATE
        if not self.attack:
            if self.movx == 0:
                state = 3
            if self.movx != 0:
                state = 5
        if self.attack:
            state = 0

        if self.death_cooldown > 0:
            state = 1

        #DETERMINE FRAME
        self.frame += 1
        if self.frame >= ANIM_ROT: self.frame = 0

        if self.frame < ANIM_ROT/5:
            frame = 0
        elif self.frame < 2*ANIM_ROT/5:
            frame = 1
        elif self.frame < 3*ANIM_ROT/5:
            frame = 2
        elif self.frame < 4*ANIM_ROT/5:
            frame = 3
        elif self.frame < ANIM_ROT:
            frame = 4

        if self.death_cooldown > 72:
            frame = 0
        elif self.death_cooldown > 54:
            frame = 1
        elif self.death_cooldown > 36:
            frame = 2
        elif self.death_cooldown > 18:
            frame = 3
        elif self.death_cooldown >= 0:
            frame = 4
            

        self.image = ELF[self.level][direction][state][frame]

    def test_gameover(self, player, flask_group, all_sprite):         
        if self.health <= 0 and self.death_cooldown == -1:
            player.skillpoints += self.points
            self.death_cooldown = 90
            self.movx = 0

        if self.death_cooldown > 0:
            self.death_cooldown -= 1
        if self.death_cooldown == 0:
            self.drop(flask_group, all_sprite)

    def drop(self, flask_group, all_sprite):
        x = randint(0,10)
        if x <= 2:
            flask_group.add(Flask(self.x, self.y, "life"))
        if x >= 8:
            flask_group.add(Flask(self.x, self.y, "mana"))
        all_sprite.add(flask_group)
        self.kill()

class Troll(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health_max = self.health = 50
        self.damages = 35
        self.points = 100
        self.nom = "troll"
        self.movx = 0
        self.movy = 0
        self.image = TROLL[0][0][3][0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.level = 0
        self.attack = False
        self.death_cooldown = -1
        self.direction = "left"
        self.attack_cooldown = 0
        self.time_attack = 0

        self.initialized = False

    def update(self, all_sprite, player, flask_group):
        if not self.initialized:
            self.collide(all_sprite, "y")
            self.initialized = True
            
        self.test_gameover(player, flask_group, all_sprite)
        self.pos_update(all_sprite, player)
        self.animation_update()

    def pos_update(self, all_sprite, player):
        
        if self.death_cooldown == -1:
            self.x += self.movx
            self.rect.x = self.x
        self.collide(all_sprite, "x")

        self.movy += 1
        self.y += self.movy
        self.rect.y = self.y
        self.collide(all_sprite, "y")

        if self.time_attack == 0:
            if self.attack_cooldown == 0:
                if abs(player.rect.x - self.rect.x) < 1500/(1920/SCREEN_SIZE[0]):
                    if abs(player.rect.y - self.rect.y) < 300/(1920/SCREEN_SIZE[0]):
                        if player.rect.x - self.rect.x < 0:
                            self.direction = "left"
                        if player.rect.x - self.rect.x > 0:
                            self.direction = "right"
                        self.charge(player, self.direction)

            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

        if self.time_attack > 0:
            if self.time_attack < 60:
                self.attack = True
            self.time_attack -= 1
            if self.time_attack == 0:
                self.movx = 0
                self.attack_cooldown = 180
                self.attack = False

    
    def collide(self, all_sprite, orientation):
        self.chute_libre = True
        contact = False
        movy = self.movy
        for o in all_sprite:
            if self.rect.colliderect(o):

                if o.nom == "platform" or o.nom == "moving_platform" or o.nom == "protection" or o.nom == "way":
                
                    if orientation == "x":
                        if self.rect.centerx > o.rect.centerx:
                            self.rect.left = o.rect.right
                            self.x = self.rect.x
                        if self.rect.centerx < o.rect.centerx:
                            self.rect.right = o.rect.left
                            self.x = self.rect.x
                        if self.time_attack != 0:
                            self.time_attack = 0
                            self.movx = 0
                            self.attack_cooldown = 180
                            self.attack = False

                    if orientation == "y":
                        if self.movy > 0 or not self.initialized:
                            self.rect.bottom = o.rect.top
                            self.y = self.rect.y
                            self.movy = 0
                            contact = True
                            self.chute_libre = False
                            if o.nom == "moving_platform":
                                self.x += o.speed
                                self.rect.x = self.x
                        if self.movy < 0:
                            self.rect.top = o.rect.bottom
                            self.y = self.rect.y
                            self.movy = 0

                if o.nom == "way":
                    if orientation == "y":
                        if self.movy >= 0:
                            if self.rect.bottom < o.rect.bottom:
                                self.rect.bottom = o.rect.top
                                self.y = self.rect.y
                                self.movy = 0
                                contact = True
                                self.chute_libre = False

                if o.nom == "fireball" or o.nom == "arrow":
                    if self.death_cooldown == -1:
                        HIT_SOUND.play()
                        self.health -= o.damages
                        o.kill()
                            
        if not contact and orientation == "y":
            self.y -= self.movy
            self.movy -= 1
            self.movy += FALL
            self.y += self.movy
            self.rect.y = self.y
            
    def animation_update(self):
        #DETERMINE DIRECTION
        if self.direction == "right":
            direction = 1
        if self.direction == "left":
            direction = 0

        #DETERMINE STATE
        if not self.attack:
            if self.movx == 0:
                state = 3
            if self.movx != 0:
                state = 4
        if self.attack:
            state = 0

        if self.death_cooldown > 0:
            state = 1

        #DETERMINE FRAME
        self.frame += 1
        if self.frame >= ANIM_ROT: self.frame = 0

        if self.frame < ANIM_ROT/5:
            frame = 0
        elif self.frame < 2*ANIM_ROT/5:
            frame = 1
        elif self.frame < 3*ANIM_ROT/5:
            frame = 2
        elif self.frame < 4*ANIM_ROT/5:
            frame = 3
        elif self.frame < ANIM_ROT:
            frame = 4

        if self.death_cooldown > 72:
            frame = 0
        elif self.death_cooldown > 54:
            frame = 1
        elif self.death_cooldown > 36:
            frame = 2
        elif self.death_cooldown > 18:
            frame = 3
        elif self.death_cooldown >= 0:
            frame = 4
            

        self.image = TROLL[self.level][direction][state][frame]

    def charge(self, player, direction):
        if direction == "left":
            self.movx = -12/(1920/SCREEN_SIZE[0])
        if direction == "right":
            self.movx = 12/(1920/SCREEN_SIZE[0])

        self.time_attack = int(abs(player.rect.x - self.rect.x)/(12/(1920/SCREEN_SIZE[0])))

    def test_gameover(self, player, flask_group, all_sprite):         
        if self.health <= 0 and self.death_cooldown == -1:
            player.skillpoints += self.points
            self.death_cooldown = 90
            self.movx = 0

        if self.death_cooldown > 0:
            self.death_cooldown -= 1
        if self.death_cooldown == 0:
            self.drop(flask_group, all_sprite)

    def drop(self, flask_group, all_sprite):
        x = randint(0,10)
        if x <= 2:
            flask_group.add(Flask(self.x, self.y, "life"))
        if x >= 8:
            flask_group.add(Flask(self.x, self.y, "mana"))
        all_sprite.add(flask_group)
        self.kill()
