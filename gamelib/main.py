from gamelib.menu.main_menu import*
from gamelib.cutscenes import*
from gamelib.loading import *


def main():
    Main_menu(screen)

def Controls(screen):
    cutscene(screen, ["CONTROLS",
    "",
    "Move: Arrow Keys",
    "Jump: Space",
    "Attack : Ctrl",
    "Select Spell : Tab",
    "",
    ""])
