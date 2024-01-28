from time import *
from pynput.keyboard import Key, Controller
from os import system, name
from pathlib import Path

import glob
import re 
import requests
import os.path
import json

keyboard = Controller()
build = "2418"

#   ______ _          _      _____      _               
#  |  ____(_)        | |    / ____|    | |              
#  | |__   _ _ __ ___| |_  | (___   ___| |_ _   _ _ __  
#  |  __| | | '__/ __| __|  \___ \ / _ \ __| | | | '_ \ 
#  | |    | | |  \__ \ |_   ____) |  __/ |_| |_| | |_) |
#  |_|    |_|_|  |___/\__| |_____/ \___|\__|\__,_| .__/ 
#                                                | |    
#                                                |_|    


uuid = ""

uuidlist = []
variables = {}
winstreak = []
apikey = ""

logpath = open("", "r")

autowhosetting = 1
username = ""


#   _____      _   _                  
#  |  __ \    | | | |                 
#  | |__) |_ _| |_| |_ ___ _ __ _ __  
#  |  ___/ _` | __| __/ _ \ '__| '_ \ 
#  | |  | (_| | |_| ||  __/ |  | | | |
#  |_|   \__,_|\__|\__\___|_|  |_| |_|
                                    
                                    
pattern = re.compile("\[Client thread/INFO\]: \[CHAT\] (.*) has joined")
pattern2 = re.compile("\[Client thread/INFO\]: \[CHAT\] (.*) has quit")
ingame = re.compile(f"\[Client thread/INFO\]: \[CHAT\] Sending you to (.*)")
who = re.compile("\[Client thread/INFO\]: \[CHAT\] ONLINE: (.*)")

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def get_lines(f):
    f.seek(0,2)
    while True:
        if line := f.readline():
            yield line
        else:
            sleep(0.05)

def autowho():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    keyboard.type('/who')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def stats(player):
    try:
        uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}').json()["id"]
        api = requests.get(f"https://api.hypixel.net/v2/player?uuid={uuid}&key={apikey}").json()["player"]

    except:
        if uuid == '': # problem here
            nick = "yes"
            variables[player] = [player, "?", "0", "0", nick]
    else:
        level = api["achievements"]["bedwars_level"]
        try:
            winstreak = api["stats"]["Bedwars"]["eight_one_winstreak"]
        except:
            winstreak = "?"
        wins = api["achievements"]["bedwars_wins"]
        variables[player] = [player, level, winstreak, wins]
    print(variables[player])

def playerdetector():
    players = []
    for line in get_lines(logpath):
        if match := ingame.search(line):
            players.clear()
            clear()
            print("Player in game")
            sleep(1)
            if autowhosetting == 1:
                autowho()

        elif match := who.search(line):
            players = re.split(', ', match.group(1))
            for player in players:
                stats(player)

        elif match := pattern.search(line):
            players.append(match.group(1))
            stats(match.group(1))

        elif match := pattern2.search(line):
            try:
                players.remove(match.group(1))
                print(players)
            except:
                print(f"{match.group(1)} not in player list, no /who?")

playerdetector()