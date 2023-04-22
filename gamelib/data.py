import os
from modules import configparser
from gamelib.config import *

#CREATE SAVE FOLDER
def set_save_folder():
    try:
        os.makedirs((SAVE_PATH))
    except:
        pass

#CURRENT LEVEL
def load_save():
    try:
        save_file = open((SAVE_PATH + "save.sav"), "r")
        niveau = int(save_file.read())
        save_file.close()
    except:
        save()
        niveau = 0
    return niveau

#SAVE CURRENT LEVEL
def save(niveau=0):
    save_file = open((SAVE_PATH + "save.sav"), "w+")
    save_file.write(str(niveau))
    save_file.close()

#CREATE DEFAULT PLAYER STATS SAVE
def init_save_player():
    save = configparser.ConfigParser()
    
    save['SKILLS'] = {}
    skill = save['SKILLS']

    skill['Fireball'] = "0"
    skill['SuperAttack'] = "0"
    skill['Protection'] = "0"
    skill['HeartPieces'] = "0"
    skill['ManaPieces'] = "0"
    skill['SkillPoints'] = "0"
            
    with open((SAVE_PATH + "save.ini"), "w+") as config:
        save.write(config)

#SAVE PLAYER STATS
def save_player(player):
    save = configparser.ConfigParser()

    save['SKILLS'] = {}
    skill = save['SKILLS']

    skill['Fireball'] = str(player.skills[0])
    skill['SuperAttack'] = str(player.skills[1])
    skill['Protection'] = str(player.skills[2])
    skill['HeartPieces'] = str(player.skills[3])
    skill['ManaPieces'] = str(player.skills[4])
    skill['SkillPoints'] = str(player.skillpoints)
        
    with open((SAVE_PATH + "save.ini"), "w+") as config:
        save.write(config)

#LOAD PLAYER STATS
def load_player():
    save = configparser.ConfigParser()
    
    save.read(SAVE_PATH + "save.ini")

    player_skills = {}

    skill = save["SKILLS"]

    player_skills["Fireball"] = skill["Fireball"]
    player_skills["SuperAttack"] = skill["SuperAttack"]
    player_skills["Protection"] = skill["Protection"]
    player_skills["HeartPieces"] = skill["HeartPieces"]
    player_skills["ManaPieces"] = skill["ManaPieces"]
    player_skills["SkillPoints"] = skill["SkillPoints"]

    return player_skills
