from time import *
import re
import requests
from pynput.keyboard import Key, Controller
import json

autowhosetting = 1

keyboard = Controller()

log = open("C:/MultiMC/instances/1.8.9/.minecraft/logs/latest.log", "r")
players = ['eviljustsnake', 'undertakerq', 'INDEKFIR858', 'Raphael825', 'MRblue_candy', 'buskapasi', 'OreoKing3', 'DBLSnowMan', 'NothingsRound', 'Bot0011', 'Teda_XD', 'ewifeymaterial', 'Mikyu__', 'ymmulc', 'Epic_Enigma', 'zHadez_']
uuidlist = []
username = "Mikyu__"

pattern = re.compile("\[Client thread/INFO\]: \[CHAT\] (.*) has joined")
pattern2 = re.compile("\[Client thread/INFO\]: \[CHAT\] (.*) has quit")
ingame = re.compile(f"\[Client thread/INFO\]: \[CHAT\] Sending you to (.*)")
who = re.compile("\[Client thread/INFO\]: \[CHAT\] ONLINE: (.*)")

key = "fc4edf76-f1af-4889-b5c0-951ab391c8ab"

winstreak = []



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

for player in players:
    try:    
        uuidget = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}').json()["id"]
        uuid = uuidget["id"]
        print(uuid)
    except:
        print("UUID not found?")
        winstreak.append("0")
    if uuid != "":    
        apiget  = requests.get(f'https://api.hypixel.net/v2/player?uuid={uuid}&key={key}').json()["player"]["stats"]["Bedwars"]["winstreak"]
        winstreak.append[apiget]