#!/usr/bin/env python3
import time
import sys
import game
from game import game_state
import tui
from tui import print3

game_state = game_state
history = game.history

if __name__ == "__main__":

    #if len(sys.argv) > 1:
        #sys.argv[1]
    print(
        "SHM Engine 1.0\n2025-10-05\nhttps://github.com/solidlamp\nThis release: 'Steamed Hams: The Game Plus! Edition 2025-10-05'"
    )

roomID = 1

def option(win, text, options, Inventory=True):
    if not hasattr(game_state, 'inventory'):
        Inventory=False
    query = 0
    choices = options
    if Inventory and hasattr(game_state, 'inventory'):
        choices = options + ["Inventory"]
    query = tui.option(win, text, choices)
    if query == "q":
        query = tui.option(win, "Are you sure you want to quit?", ["Yes", "No"])
        if query == 0 or query == "q":
            sys.exit()
        else:
            query = option(win, text, options, Inventory=True)
    elif Inventory and query == choices.index("Inventory"):
        win.clear()
        print3(win, "\n" + str(game_state.inventory))
        print3(win, "\nPress any key to exit inventory.")
        win.getch()
        query = option(win, text, options, Inventory=True)
    return query

def ending(win, end):
    if hasattr(game, 'endingText') and end in game.endingText:
        print3(win, "\n" + game.endingText[end].replace("|", end), 0, 0.015, 0.65)
    time.sleep(1.5)
    win.clear()
    print3(win, game.defaultEnding.replace("|", end), 0, 0.015, 0.65)
    time.sleep(3.5)

def lose(win, lose):
    time.sleep(0.25)
    if hasattr(game, 'loseText') and lose in game.loseText:
        printText = "\n" + game.loseText[lose].replace("|", lose)
    else:
        printText = game.defaultLose.replace("|", lose)
    print3(win, printText, 0, 0.015, 0.65)
    win.clear()
    time.sleep(0.5)
    query = tui.option(win, printText + "Try again?", ["Yes", "No"])
    if query == 1 or query == "q":
        sys.exit()
    else:
        return 1

def gameLoop(win, starting_room=0):
    rooms = game.get_rooms(win)
    win.clear()
    if game.gameInfo["complevel"] != 1:
        complevel = game.gameInfo["complevel"]
        print3(win, f"ERROR: This game (complevel {complevel}) is not compatible with this version of the SHM Engine (1.0 / complevel 1).", 31, 0)
        print3(win, "\nPress any key to exit...", 0, 0)
        win.getch()
        sys.exit(1)
    global roomID
    if starting_room:
        roomID = starting_room
    room = rooms[roomID]
    text = ""
    if "Requirements" in room and not room["Requirements"]():
        print3(win, room["AlternateText"])
        text = room["AlternateText"]
    else:
        print3(win, room["Text"])
        text = room["Text"]
    if "Script" in room:
        room["Script"]()
    if "Ending" in room:
        ending(win, room["Ending"])
        roomID = 1
        return 1
    if "Item" in room:
        if (
            "ItemRequirements" in room
            and room["ItemRequirements"]()
            or "ItemRequirements" not in room
        ):
            if "ItemText" in room:
                print3(win, "\n" + room["ItemText"])
            if hasattr(game_state, 'inventory') and game.keyItems and room["Item"] in game.keyItems:
                game_state.inventory.getKeyItem(room["Item"], win)
            elif hasattr(game_state, 'inventory'):
                game_state.inventory.getItem(room["Item"], win)
            win.getch()
    if "Automove" in room:
        if isinstance(room["Automove"], tuple) and room["Automove"][0] == "history":
            roomID = history[room["Automove"][1]]
        elif isinstance(room["Automove"], int):
            roomID = room["Automove"]
        time.sleep(1)
    elif "Move" in room:
        OptionsIndex = []
        Options = []
        for i in room["Move"]:
            OptionRequirements = "Option" + str(room["Move"].index(i)) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                OptionsIndex.append(i)
                Options.append(room["Options"][room["Move"].index(i)])
        if "Inventory" in room and game_state.inventory and not room["Inventory"]:
            query = option(win, text, Options, Inventory=False)
        else:
            query = option(win, text, Options)
        roomID = OptionsIndex[query]
    history.append(roomID)
    if len(history) > 10:
        history.pop(0)
    if "Lose" in room:
        roomID = lose(win, room["Lose"])
    return 0
