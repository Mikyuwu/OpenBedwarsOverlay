from time import *
import re
import requests
from pynput.keyboard import Key, Controller
import json

keyboard = Controller()

log = open("C:/MultiMC/instances/1.8.9/.minecraft/logs/latest.log", "r")

uuid = ""


players = ['eviljustsnake', 'undertakerq', 'INDEKFIR858', 'Raphael825', 'MRblue_candy', 'buskapasi', 'OreoKing3', 'DBLSnowMan', 'NothingsRound', 'Bot0011', 'Teda_XD', 'ewifeymaterial', 'Mikyu__', 'ymmulc', 'Epic_Enigma', 'zHadez_']
uuidlist = []
variables = {}
winstreak = []
key = "fc4edf76-f1af-4889-b5c0-951ab391c8ab"

autowhosetting = 1
username = "Mikyu__"

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

def playerdetector():
    for line in get_lines(log):
        if match := ingame.search(line):
            players.clear()
            print("Player in game")
            sleep(2)
            if autowhosetting == 1:
                autowho()

        elif match := who.search(line):
            players = re.split(', ', match.group(1))
            print(players)

        elif match := pattern.search(line):
            players.append(match.group(1))
            print(players)

        elif match := pattern2.search(line):
            try:
                players.remove(match.group(1))
                print(players)
            except:
                print(f"{match.group(1)} not in player list, no /who?")

def stats():
    for player in players:    
        try:
            uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}').json()["id"]
            api = requests.get(f"https://api.hypixel.net/v2/player?uuid={uuid}&key={key}").json()["player"]

        except:
            if uuid == '': 
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