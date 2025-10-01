import time
from dataclasses import dataclass
import random
import sys
import tui
print3 = tui.print3


gameInfo = {
    "complevel": 1,
    "abbr": "SHM",
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
    rooms = {
        0: {
            "Text": "Choose your path.",
            "Options": ["Skinner", "Chalmers"],
            "Move": [1, 100],
        },
        1: {
            "Text": "*\033[33m*Ding, dong!*\033[0m There goes the doorbell.\nOpen it?",
            "Options": ["Yes", "No"],
            "Move": [5, 2],
        },
        2: {
            "Text": "You did not open the door.\n\033[33m*Ding, dong!*\033[0m There goes the doorbell, again.\nOpen it?",
            "Options": ["Yes", "No"],
            "Move": [5, 3],
        },
        3: {
            "Text": "You did not open the door.\n\033[33m*Ding, dong!*\033[0m There goes the doorbell, again.\n\033[34mChalmers: 'Seymour!'\033[0m\nOpen it?",
            "Options": ["Yes", "No"],
            "Move": [5, 4],
        },
        4: {
            "Text": "You did not open the door.",
            "Ending": "Boring",
        },
        5: {
            "Text": "\033[34mChalmers: 'Well, Seymour, I made it, despite your directions.'\033[0m",
            "Options": ["Aggressive and rude insult","Overly friendly greeting","Shut the door","Beatbox","[Say nothing]"],
            "Move": [6, 10, 7, 8, 9],
        },
        6: {
            "Text": "\033[36mSkinner: 'You fat-headed buffoon! The directions I gave you were perfectly in order! Plus you've already been here, so you must know the way!'\033[0m\n\033[34mChalmers: 'Seymour! I have never been more insulted in my life! You're fired!'\033[0m",
            "Lose": "Fired",
        },
        9: {
            "Text": "\033[34mChalmers: '...Yeah.'\033[0m",
            "Script": lambda: time.sleep(0.5),
            "Automove": 11,
        },
        10: {
            "Text": "\033[36mSkinner: 'Ah, Superintendent Chalmers, welcome! I hope you're prepared for an unforgettable luncheon!'\033[0m\n\033[34mChalmers: '...Yeah.'\033[0m",
            "Automove": 11,
        },
        11: {
            "Text": "\033[1mThe Kitchen\033[0m\n+---------+",
            "Script": lambda: time.sleep(0.5),
            "Automove": 12,
        },
        12: {
            "Text": "*The roast burned whilst in the oven*\n\033[36mSkinner: 'Oh, egads! My roast is ruined!'\033[0m",
            "Options": ["Tell the truth","Lie and purchase fast food","Serve ruined roast","Serve the roast anyway, and ignore the fact that it is ruined"],
            "Move": [13, 14, 107, 108]
        },
        13: {
            "Text": "\033[36mSkinner: 'Superintendent! The roast is on fire!'\n\033[34mChalmers: 'Good lord! We must put it out!'\033[0m\n*Skinner and Chalmers extinguish the fire before any harm occurs.*\n\033[34mChalmers: Well, Seymour, we saved the house, but the roast is unrecoverable.\n\033[36mSkinner: 'Well, there's a Krusty Burger just down the street. We could have our lunch there?'\n\033[34mChalmers: 'Krusty Burger? I do enjoy fast food from time to time, and eating does help take your mind off things, especially incidents like this.'\n\033[36mSkinner: 'I could just go get them now and we could eat them in the dining room?'\n\033[34mChalmers: 'Oh, Seymour, you don't need to do that - we can just eat at the restaurant.'\n\033[36mSkinner: 'No, no - it's really no issue. Just wait here whilst I order.'\033[0m\n*Skinner and Chalmers enjoy a luncheon of Krusty Burgers together*\n\033[34mChalmers: 'Well, Seymour, that was delicious, but I really must be going now. Perhaps we can pick this up another time?'\033[0m",
            "Ending": "Honest Abe",
        },
    }
    return rooms
##
