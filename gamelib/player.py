import pygame
from random import *

from gamelib.config import *
from gamelib.loading import *
from gamelib.data import *
from gamelib.sprites import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.nom = "player"
        self.movy = 0
        self.movx = 0
        self.jump_mode = False
        self.chute_libre = True
        self.attack_mode = False
        self.win = False
        self.game_over = False
        self.hit_cooldown = 0
        self.skin = 0
        self.attack_cooldown = 0
        self.super_attack_mode = False
        self.death_cooldown = -1

        #ANIMATION INIT
        self.image = PLAYER[self.skin][1][3][0]
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.height = 165/(1920/SCREEN_SIZE[0])
        self.rect.width = 165/(1920/SCREEN_SIZE[0])

        #POSITION INIT
        self.direction = "right"
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        #LOAD PLAYER STATS
        try:
            load = load_player()
        except:
            init_save_player()
            load = load_player()
            
        self.skillpoints = int(load['SkillPoints'])
        self.skills = [int(load["Fireball"]),
                       int(load["SuperAttack"]),
                       int(load["Protection"]),
                       int(load["HeartPieces"]),
                       int(load["ManaPieces"])]

        self.health_max = 100 + self.skills[3]*20
        self.mana_max = 50 + self.skills[4]*10
        self.health = self.health_max
        self.mana = self.mana_max

        self.initialized = False

    def update(self, up, left, right, attack, level, camera):
        if not self.initialized:
            self.collide(level.all_sprite, "y")
            self.initialized = True
        
        self.test_gameover(camera)
        self.pos_update(up, left, right, attack, level)
        self.animation_update(up, left, right)

    def pos_update(self, up, left, right, attack, level):

        if not self.super_attack_mode:
            if attack and self.attack_cooldown == 0:
                self.attack()
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            if self.attack_cooldown == 6:
                ATTACK_SOUND.play()
                level.spells_group.add(Fireball(self))
                level.all_sprite.add(level.spells_group)

        if self.super_attack_mode:
            if self.attack_cooldown == 0:
                self.super_attack_mode = False
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            if self.attack_cooldown == 6:
                for i in range(5 + self.skills[1]*3):
                    x = randint(int(self.rect.x-SCREEN_SIZE[0]/10), int(self.rect.x+6*SCREEN_SIZE[0]/10))
                    y = randint(int(self.rect.y-2*SCREEN_SIZE[1]), int(self.rect.y-SCREEN_SIZE[1]))
                    level.spells_group.add(SuperFireball(self, x, y))
                    level.all_sprite.add(level.spells_group)

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        if not left and not right:
            self.movx = 0

        if self.death_cooldown == -1:
            if left or right:
                if left:
                    self.movx = -SPEED
                    self.direction = "left"
                if right:
                    self.movx = SPEED
                    self.direction = "right"
                self.x += self.movx
                self.rect.x = self.x
            self.collide(level.all_sprite, "x")

        self.movy += 1
        self.y += self.movy
        self.rect.y = self.y
        self.collide(level.all_sprite, "y")


    def collide(self, all_sprite, orientation):
        self.chute_libre = True
        contact = False
        movy = self.movy
        for o in all_sprite:
            if self.rect.colliderect(o):

                if o.nom == "platform" or o.nom == "moving_platform":
                
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
                            if self.jump_mode:
                                self.jump_mode = False
                            if o.nom == "moving_platform":
                                self.x += o.speed
                                self.rect.x = self.x
                        if self.movy < 0:
                            contact = True
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
                                if self.jump_mode:
                                    self.jump_mode = False

                if o.nom == "warrior" or o.nom == "elf" or o.nom == "troll" or o.nom == "ork":
                    if self.hit_cooldown == 0:
                        if o.death_cooldown == -1:
                            self.get_hit(o.damages)

                if o.nom == "arrow":
                    if self.hit_cooldown == 0:
                        self.get_hit(o.damages)
                        o.kill()

                if o.nom == "life" or o.nom == "mana":
                    if o.nom == "life":
                        self.health += 30
                        if self.health > self.health_max:
                            self.health = self.health_max
                    if o.nom == "mana":
                        self.mana += 20
                        if self.mana > self.mana_max:
                            self.mana = self.mana_max
                    o.kill()
                        
                            
        if not contact and orientation == "y":
            self.y -= self.movy
            self.movy -= 1
            self.movy += FALL
            self.y += self.movy
            self.rect.y = self.y

    def animation_update(self, up, left, right):
        
        #DETERMINE DIRECTION
        if self.direction == "right":
            direction = 1
        if self.direction == "left":
            direction = 0

        #DETERMINE ACTION
        if (left or right) or (not left and not right):
            if not left and not right:
                state = 3
            if left or right:
                state = 5
                
            #FRAME
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

        #DETERMINE ACTION 
        if self.jump_mode:
            state = 4

            #FRAME
            if self.movy < 3*JUMP/5:
                frame = 1
            elif self.movy < JUMP/5:
                frame = 2
            elif self.movy < -JUMP/5:
                frame = 3
            elif self.movy < -3*JUMP/5:
                frame = 4

        if self.hit_cooldown > 95:
            state = 2

            if self.hit_cooldown > 115:
                frame = 0
            elif self.hit_cooldown > 110:
                frame = 1
            elif self.hit_cooldown > 105:
                frame = 2
            elif self.hit_cooldown > 100:
                frame = 3
            elif self.hit_cooldown > 95:
                frame = 4

        if self.attack_cooldown > 0:
            state = 0

            if self.attack_cooldown > 24:
                frame = 0
            elif self.attack_cooldown > 18:
                frame = 1
            elif self.attack_cooldown > 12:
                frame = 2
            elif self.attack_cooldown > 6:
                frame = 3
            elif self.attack_cooldown > 0:
                frame = 4

        if self.death_cooldown >= 0:
            state = 1

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
         
        self.image = PLAYER[self.skin][direction][state][frame]
            

    def test_gameover(self, camera):
        if self.rect.top > camera.world_rect.bottom:
            self.game_over = True
            
        if self.health <= 0 and self.death_cooldown == -1:
            self.death_cooldown = 90

        if self.death_cooldown > 0:
            self.death_cooldown -= 1
        if self.death_cooldown == 0:
            self.game_over = True

    def jump(self, all_sprite):
        if not self.chute_libre:
            self.movy = JUMP
            self.chute_libre = True
            self.jump_mode = True

    def attack(self):
        self.attack_cooldown = 30

    def protection(self, level):
        if self.mana >= 10:
            self.mana -= 10
            level.spells_group.add(Protection(self))
            level.all_sprite.add(level.spells_group)

    def super_attack(self):
        if self.mana >= 50:
            self.mana -= 50
            self.attack_cooldown = 30
            self.super_attack_mode = True

    def get_hit(self, damages):
        HURT_SOUND.play()
        self.hit_cooldown = 120
        self.health -= damages
        
