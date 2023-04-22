import pygame
from pygame.locals import *
from gamelib.config import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF, 32)
pygame.mouse.set_visible(0)
pygame.display.set_caption("Wizard")
pygame.display.set_icon(pygame.image.load("Icon.ico"))

#MUSIC INIT
pygame.mixer.music.load("data/musics/menu.ogg")
pygame.mixer.music.play(-1)

from gamelib.loading_screen import *
ld = 0
load_screen(screen, ld)

"""SYSTEM"""

ICON = pygame.image.load("Icon.ico")
CURSOR = pygame.image.load("data/cursor.cur").convert_alpha()

FONT16 = pygame.font.Font(("data/fonts/font.ttf"), int(16/(1920/SCREEN_SIZE[0])))
FONT48 = pygame.font.Font(("data/fonts/font.ttf"), int(48/(1920/SCREEN_SIZE[0])))
FONT = [FONT16, FONT48]


"""SOUNDS"""

CLICK_SOUND = pygame.mixer.Sound("data/sounds/click.wav")
MENU_SOUND = pygame.mixer.Sound("data/sounds/menu.wav")
ATTACK_SOUND = pygame.mixer.Sound("data/sounds/attack.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("data/sounds/gameover.wav")
HURT_SOUND = pygame.mixer.Sound("data/sounds/hurt.wav")
HIT_SOUND = pygame.mixer.Sound("data/sounds/hit.wav")

"""MUSICS"""




load_screen(screen, ld)
"""PLAYER"""

PLAYER = [[[[]for k in range(7)]for j in range(2)]for i in range(3)]
for i in range(1):
    l = 0
    for j in ("/left/", "/right/"):
        f = 0
        for k in ("ATTACK/ATTACK_00", "DIE/DIE_00", "HURT/HURT_00", "IDLE/IDLE_00", "JUMP/JUMP_00", "RUN/RUN_00", "WALK/WALK_00"):
            for m in range(5):
                PLAYER[i][l][f].append(pygame.image.load("data/assets/player/" + str(i+1) + j + k + str(m) + ".png").convert_alpha())
                PLAYER[i][l][f][m] = pygame.transform.scale(PLAYER[i][l][f][m], (int(PLAYER[i][l][f][m].get_width()*PLAYER_SIZE), int(PLAYER[i][l][f][m].get_height()*PLAYER_SIZE)))
            f += 1       
        l += 1
    ld += 1
    load_screen(screen, ld)



"""IVENTORY"""

CIRCLES = []
for i in range(3):
    CIRCLES.append(pygame.image.load("data/assets/inventory/" + str(i) + ".png").convert_alpha())
    CIRCLES[i] = pygame.transform.scale(CIRCLES[i], (int(100/(1920/SCREEN_SIZE[0])), int(100/(1920/SCREEN_SIZE[0]))))

ld += 1
load_screen(screen, ld)

"""SPELLS"""

SPELLS = []
j = 0
for i in ("blue", "pink", "red"):
    SPELLS.append(pygame.image.load("data/assets/spells/" + i + ".png").convert_alpha())
    SPELLS[j] = pygame.transform.scale(SPELLS[j], (int(90/(1920/SCREEN_SIZE[0])), int(34/(1920/SCREEN_SIZE[0]))))
    j += 1

PLUS = pygame.image.load("data/assets/+.png").convert_alpha()
PLUS = pygame.transform.scale(PLUS, (int(20/(1920/SCREEN_SIZE[0])), int(20/(1920/SCREEN_SIZE[0]))))

SUPER_SPELL = []
j = 0
for i in ("blue", "pink", "red"):
    SUPER_SPELL.append(pygame.image.load("data/assets/spells/Super" + i + ".png").convert_alpha())
    SUPER_SPELL[j] = pygame.transform.scale(SUPER_SPELL[j], (int(90/(1920/SCREEN_SIZE[0])), int(34/(1920/SCREEN_SIZE[0]))))
    j += 1


ld += 1
load_screen(screen, ld)


ARROW_RIGHT = pygame.image.load("data/assets/enemies/Elf/1/arrow_right.png").convert_alpha()
ARROW_RIGHT = pygame.transform.scale(ARROW_RIGHT, (int(ARROW_RIGHT.get_width()/5/(1920/SCREEN_SIZE[0])), int(ARROW_RIGHT.get_height()/5/(1920/SCREEN_SIZE[0]))))
ARROW_LEFT = pygame.image.load("data/assets/enemies/Elf/1/arrow_left.png").convert_alpha()
ARROW_LEFT = pygame.transform.scale(ARROW_LEFT, (int(ARROW_LEFT.get_width()/5/(1920/SCREEN_SIZE[0])), int(ARROW_LEFT.get_height()/5/(1920/SCREEN_SIZE[0]))))
ARROW = [ARROW_LEFT, ARROW_RIGHT]

FIREBALL = [[[]for j in range(2)]for i in range(3)]
L = 0
for i in ("blue/", "pink/", "red/"):
    l = 0
    for j in ("left/", "right/"):
        for k in range(6):
            FIREBALL[L][l].append(pygame.image.load("data/assets/spells/" + i + j + str(k+1) + ".png").convert_alpha())
            FIREBALL[L][l][k] = pygame.transform.scale(FIREBALL[L][l][k], (int(FIREBALL[L][l][k].get_width()/3/(1920/SCREEN_SIZE[0])), int(FIREBALL[L][l][k].get_height()/3/(1920/SCREEN_SIZE[0]))))
        l += 1
    L += 1
    ld += 1
    load_screen(screen, ld)

PROTECTION = pygame.image.load("data/assets/spells/protection.png")
PROTECTION_SPELL = pygame.transform.scale(PROTECTION, (int(PROTECTION.get_width()/(1920/SCREEN_SIZE[0])/5), int(PROTECTION.get_height()/(1920/SCREEN_SIZE[0])/5)))
PROTECTION = pygame.transform.scale(PROTECTION, (int(PROTECTION.get_width()/(1920/SCREEN_SIZE[0])), int(PROTECTION.get_height()/(1920/SCREEN_SIZE[0]))))

SUPER = [[]for i in range(3)]
L = 0
for i in ("blue/", "pink/", "red/"):
    for j in range(6):
        SUPER[L].append(pygame.image.load("data/assets/spells/super/" + i + str(j+1) + ".png").convert_alpha())
        SUPER[L][j] = pygame.transform.scale(SUPER[L][j], (int(SUPER[L][j].get_width()/2/(1920/SCREEN_SIZE[0])), int(SUPER[L][j].get_height()/2/(1920/SCREEN_SIZE[0]))))
    L += 1
    ld += 1
    load_screen(screen, ld)

"""ITEMS"""

LIFE_POTION = pygame.image.load("data/assets/items/life.png").convert_alpha()
LIFE_FLASK = pygame.transform.scale(LIFE_POTION, (int(LIFE_POTION.get_width()/(1920/SCREEN_SIZE[0])/4), int(LIFE_POTION.get_height()/(1920/SCREEN_SIZE[0])/4)))
LIFE_POTION = pygame.transform.scale(LIFE_POTION, (int(LIFE_POTION.get_width()/(1920/SCREEN_SIZE[0])/5), int(LIFE_POTION.get_height()/(1920/SCREEN_SIZE[0])/5)))
MANA_POTION = pygame.image.load("data/assets/items/mana.png").convert_alpha()
MANA_FLASK = pygame.transform.scale(MANA_POTION, (int(MANA_POTION.get_width()/(1920/SCREEN_SIZE[0])/4), int(MANA_POTION.get_height()/(1920/SCREEN_SIZE[0])/4)))
MANA_POTION = pygame.transform.scale(MANA_POTION, (int(MANA_POTION.get_width()/(1920/SCREEN_SIZE[0])/5), int(MANA_POTION.get_height()/(1920/SCREEN_SIZE[0])/5)))


ld += 1
load_screen(screen, ld)
"""MENU"""

TITLE = pygame.image.load("data/Title.png").convert()
TITLE = pygame.transform.scale(TITLE, SCREEN_SIZE)

MAP = pygame.image.load("data/map.png").convert()
MAP = pygame.transform.scale(MAP, SCREEN_SIZE)

MAPLEVEL = []
for i in range(4):
    MAPLEVEL.append(pygame.image.load("data/assets/levels/level_" + str(i+1) + ".png").convert_alpha())
    MAPLEVEL[i] = pygame.transform.scale(MAPLEVEL[i], (int(MAPLEVEL[i].get_width()*PLAYER_SIZE), int(MAPLEVEL[i].get_height()*PLAYER_SIZE)))


ld += 1
load_screen(screen, ld)
"""ENEMIES"""

TROLL = [[[[]for k in range(7)]for j in range(2)]for i in range(3)]
ORK = [[[[]for k in range(7)]for j in range(2)]for i in range(3)]
WARRIOR = [[[[]for k in range(7)]for j in range(2)]for i in range(3)]
ELF = [[[[]for k in range(7)]for j in range(2)]for i in range(3)]
for i in range(1):
    l = 0
    for j in ("/left/", "/right/"):
        f = 0
        for k in ("ATTACK/ATTACK_00", "DIE/DIE_00", "HURT/HURT_00", "IDLE/IDLE_00", "RUN/RUN_00", "WALK/WALK_00"):
            for m in range(7):
                TROLL[i][l][f].append(pygame.image.load("data/assets/enemies/Troll/" + str(i+1) + j + k + str(m) + ".png").convert_alpha())
                TROLL[i][l][f][m] = pygame.transform.scale(TROLL[i][l][f][m], (int(TROLL[i][l][f][m].get_width()*PLAYER_SIZE), int(TROLL[i][l][f][m].get_height()*PLAYER_SIZE)))

                ORK[i][l][f].append(pygame.image.load("data/assets/enemies/Ork/" + str(i+1) + j + k + str(m) + ".png").convert_alpha())
                ORK[i][l][f][m] = pygame.transform.scale(ORK[i][l][f][m], (int(ORK[i][l][f][m].get_width()*PLAYER_SIZE/4), int(ORK[i][l][f][m].get_height()*PLAYER_SIZE/4)))

            for m in range(5):
                WARRIOR[i][l][f].append(pygame.image.load("data/assets/enemies/Warrior/" + str(i+1) + j + k + str(m) + ".png").convert_alpha())
                WARRIOR[i][l][f][m] = pygame.transform.scale(WARRIOR[i][l][f][m], (int(WARRIOR[i][l][f][m].get_width()*PLAYER_SIZE/2), int(WARRIOR[i][l][f][m].get_height()*PLAYER_SIZE/2)))

                ELF[i][l][f].append(pygame.image.load("data/assets/enemies/Elf/" + str(i+1) + j + k + str(m) + ".png").convert_alpha())
                ELF[i][l][f][m] = pygame.transform.scale(ELF[i][l][f][m], (int(ELF[i][l][f][m].get_width()*PLAYER_SIZE/3), int(ELF[i][l][f][m].get_height()*PLAYER_SIZE/3)))
            f += 1
            ld += 1
            load_screen(screen, ld)
        l += 1

"""LEVELS"""

BLOCK = pygame.image.load("data/assets/levels/block.png").convert_alpha()
BLOCK = pygame.transform.scale(BLOCK, (BLOCK_SIZE, BLOCK_SIZE))

MOVING_PLATFORM = pygame.image.load("data/assets/levels/moving_platform.png").convert_alpha()
MOVING_PLATFORM = pygame.transform.scale(MOVING_PLATFORM, (int(MOVING_PLATFORM.get_width()/(1920/SCREEN_SIZE[0])), int(MOVING_PLATFORM.get_height()/(1920/SCREEN_SIZE[0]))))

WAY = pygame.image.load("data/assets/levels/way.png").convert_alpha()
WAY = pygame.transform.scale(WAY, (BLOCK_SIZE*2, BLOCK_SIZE))

LEVEL1 = []
LEVEL2 = []
LEVEL3 = []
LEVEL4 = []
for i in range(7):
    LEVEL1.append(pygame.image.load("data/assets/levels/level1/" + str(i+1) + ".png").convert_alpha())
    LEVEL1[i] = pygame.transform.scale(LEVEL1[i], SCREEN_SIZE)

ld += 1
load_screen(screen, ld)

for i in range(9):
    LEVEL2.append(pygame.image.load("data/assets/levels/level2/" + str(i+1) + ".png").convert_alpha())
    LEVEL2[i] = pygame.transform.scale(LEVEL2[i], SCREEN_SIZE)

ld += 1
load_screen(screen, ld)

for i in range(8):
    LEVEL3.append(pygame.image.load("data/assets/levels/level3/" + str(i+1) + ".png").convert_alpha())
    LEVEL3[i] = pygame.transform.scale(LEVEL3[i], SCREEN_SIZE)

ld += 1
load_screen(screen, ld)

for i in range(5):
    LEVEL4.append(pygame.image.load("data/assets/levels/level4/" + str(i+1) + ".png").convert_alpha())
    LEVEL4[i] = pygame.transform.scale(LEVEL4[i], SCREEN_SIZE)

ld += 1
load_screen(screen, ld)
