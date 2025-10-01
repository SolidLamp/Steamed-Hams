import time
from dataclasses import dataclass
import random
import sys
import tui
print3 = tui.print3


gameInfo = {
    "complevel": 0,
    "abbr": "TSQ",
    "title": "Steamed Hams: The Game Plus! Edition",
    "desc": "An adventure meme game where you take multiple paths to create an unforgettable luncheon.",
    "inventory": False
}

history = []

endingText = {
    "Good": "And so, overnight, all the people returned to the village, as if they had never left.\nSoon after, the village was lifted into high spirits as the harvest had been the best in almost thirty years.\nDespite the prospering village, you decided to leave.\nYou had no desire to stay after the events you just experienced, and you would rather leave than stay to make some money.",
    "Secret": "And so, overnight, you became the new shopkeeper, but nothing really changed in the end.\nThe villagers never returned, but many travellers came, hearing about what happened.\nMany decided to stay after a plentiful harvest brought good omens to the village.\nThis, however, would not be the last of it...\n...and you knew that.",
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
}
defaultEnding = "You achieved the\n|\nEnding."

@dataclass
class Inventory:
    items: list[str] = None
    keyItems: list[str] = None

    def __post_init__(self):
        self.items = [] if self.items is None else self.items
        self.keyItems = [] if self.keyItems is None else self.keyItems

    def getItem(self, item: str, win):
        print3(win, "\nYou got \033[1m" + str(item) + "\033[0m!\n")
        self.items.append(item)
        print3(win, "Press any button to continue...")
        win.getch()

    def getKeyItem(self, item: str, win):
        print3(win, "\nYou got \033[1m\033[47m" + str(item) + "\033[0m!\n")
        self.keyItems.append(item)
        print3(win, "Press any button to continue...")
        win.getch()

    def __str__(self):
        if not self.items and not self.keyItems:
            return "Your inventory is empty"
        output = []
        if self.items:
            output.append("Items:\n" + "\n".join(f"- {item}" for item in self.items))
        if self.keyItems:
            output.append(
                "Key Items:\n" + "\n".join(f"- {item}" for item in self.keyItems)
            )
        return "\n".join(output)


@dataclass
class gameState:
    inventory: Inventory
    rubies: int = 0
    shopkeeperName: str = "The Shopkeeper"
    position: float = 0.0
    beatenGame: bool = False
    caveOpened: bool = False
    fletcherOpen: bool = True

    def getRuby(self, obtained: int, win):
        print3(win, "\nYou got \033[1m" + str(obtained) + "\033[0m Rubies!")
        self.rubies += obtained
        print3(win,
            "\033[0m\n You currently have \033[1m"
            + str(self.rubies)
            + "\033[0m Rubies.\n"
        )
        print3(win, "Press any button to continue...")
        win.getch()


game_state = gameState#(inventory=Inventory(items=[]))


def itemEvaluation():
    cursedItems = len(
        {"Rusted Sword", "Amber Necklace", "Golden Idol"}
        & set(game_state.inventory.keyItems)
    )
    return cursedItems

def ShopkeeperFinalSpeech(win):
    print3(win,
            "\033[33m'Well, I'll be. That's all of them. Honestly, I kind of doubted you could do it - now I see that my doubt was misplaced! You will go down in legend for your heroism!'"
        )
    time.sleep(0.75)
    print3(win, "\033[33m\n'Oh, and just one more thing: thank you.'\033[0m")
    time.sleep(1.5)

def ShopkeeperAffirmations(win):
    cursedItems = len(
        {"Rusted Sword", "Amber Necklace", "Golden Idol"}
        & set(game_state.inventory.keyItems)
    )
    print3(win,
            f"\033[33m'Great! You managed to get {cursedItems} of the items - now we just need {3 - cursedItems} more!'\033[0m"
    )


def fishEvaluation(win):
    fishBought = len(
        {
            "Fillet of Cod",
            "Fillet of Salmon",
            "Smoked Trout",
            "Jar of Tuna",
            "Fillet of Smoked Haddock",
        }
        & set(game_state.inventory.keyItems)
    )
    if fishBought >= 1 and "Fishing Rod" not in game_state.inventory.keyItems:
        print3(win,
            "\033[36m'You know, I recently got a new fishing rod. Say, you can have my old one, since you bought something.'\033[0m"
        )
        game_state.inventory.getKeyItem("Fishing Rod", win)
    else:
        print3(win,
            "\033[36m'You know, I'd be more in the mood to talk if you bought something.'\033[0m"
        )


def mineralEvaluation(win):
    for item in [
        item for item in list(game_state.inventory.items) if item in list(mysticalRocks)
    ]:  # This is not that readable but it does stuff basically]
        value = mysticalRocks[item]
        game_state.getRuby(value, win)
        game_state.inventory.items.remove(item)
    print3(win,
        "\033[32m'Thank you so much. These will be excellent to add to my collection.'\033[0m"
    )

def debug(win):
    game_state.inventory.getKeyItem("Rusted Sword", win)
    game_state.inventory.getKeyItem("Amber Necklace", win)
    game_state.inventory.getKeyItem("Golden Idol", win)
    game_state.inventory.getKeyItem("Ancient Key", win)
    game_state.inventory.getKeyItem("Fishing Rod", win)
    game_state.inventory.getKeyItem("Bow and Arrow", win)
    game_state.inventory.getKeyItem("Silver Amulet", win)
    game_state.inventory.getItem("Lamp Oil", win)
    game_state.inventory.getItem("Lamp Oil", win)
    game_state.inventory.getItem("Rope", win)
    game_state.inventory.getItem("Bomb", win)
    game_state.inventory.getItem("Bomb", win)
    game_state.getRuby(9001, win)

def get_rooms(win):
def get_rooms(win):
    rooms = {
        0: {
            "Text": "Choose your path.",
            "Options": ["Skinner", "Chalmers"],
            "Move": [1, 100],
        },
        1: {
            "Text": "[Ding, dong!] There goes the doorbell.\nOpen it?",
            "Options": ["Yes", "No"],
            "Move": [5, 2],
        },
        2: {
            "Text": "You did not open the door.\n[Ding, dong!] There goes the doorbell, again.\nOpen it?",
            "Options": "[Yes", "No"],
            "Move": [5, 3],
        },
        3: {
            "Text": "You did not open the door.\n[Ding, dong!] There goes the doorbell, again.\n\033[34mChalmers: "Seymour!"\033[0m\nOpen it?",
            "Options": ["Yes", "No"],
            "Move": [5, 4],
        },
        4: {
            "Text": "You did not open the door.",
            "Ending": "Boring",
        },
        5: {
            "Text": "\033[34mChalmers: Well, Seymour, I made it, despite your directions.\033[0m",
            "Options": ["Aggressive and rude insult","Overly friendly greeting","Shut the door","Beatbox","[Say nothing]"]
            "Move": [6, 10, 7, 8, 9],
        },
        6: {
            "Text": "You did not open the door.",
            "Ending": "Boring",
        },
    }
    return rooms
##
