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
    endings = []
    luncheon = 'steamed clams'


game_state = gameState#(inventory=Inventory(items=[]))

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
        14: {
            "Text": "\033[36mSkinner: 'But what if I were to purchase fast food and disguise it as my own cooking? [chuckles] Delightfully devilish, Seymour.'\033[0m\n*Chalmers enters the kitchen, viewing Skinner attempting to escape out of the window*\n\033[34mChalmers: 'SEEEEEYMOOUUURRR!!!'\033[0m",
            "Options": ["Tell the truth","Opening a window","Stretching your calves on the windowsill","Skydiving out of the window","Tell the truth, but play it off as a joke"],
            "Move": [15, 16, 18, 17, 19]
        },
        15: {
            "Text": "\033[36mSkinner: 'Superintendent! The roast is on fire, I-'\n\033[34mChalmers: 'And you were climbing out of the window to escape?'\n\033[36mSkinner: 'No, I was just-'\n\033[34mChalmers: 'Good lord, Seymour! Aren't you a member of the Springfield Voluntary Fire Department? You haven't alerted me or your mother! We could have been seriously injured!'\n\033[36mSkinner: 'Well, now that you put it like that, I suppose-'\n\033[34mChalmers: That's it, Seymour! You're fired!'\033[0m",
            "Lose": "Fired",
        },
        16: {
            "Text": "Skinner: 'Superintendent! I was just opening a window to let the smoke out.'\033[34mChalmers: 'Smoke? What smoke? Good lord, the oven is on fire!'\033[36mSkinner: 'Uh, I meant that I was, uh-'\033[34mChalmers: 'Seymour, you were clearly climbing out of the window to escape!'\n\033[36mSkinner: 'Ooh, uh, I was, uh, just, um-'\n\033[34mChalmers: 'That's it, Seymour! If I can't trust you not to neglect even the one guest at a small meal event, how can I trust you not to neglect the children at the school? I'm firing you for lack of safety and neglect!'\033[0m",
            "Lose": "Fired",
        },
        17: {
            "Text": "\033[36mSkinner: 'Superintendent! I was just skydiving out of the window!'\n\033[34mChalmers: 'What?'\033[0m",
            "Ending": "What",
        },
        18: {
            "Text": "\033[36mSkinner: 'Superintendent! I was just, uh, just stretching my calves on the windowsill. Isometric exercise! Care to join me?'\n\033[34mChalmers: 'Why is there smoke coming out of your oven, Seymour?'\033[0m",
            "Options": ["Tell the truth","Make up an excuse","Deny the existence of the smoke","Crack a joke"],
            "Move": [20, 21, 22, 23],
        },
        19: {
            "Text": "\033[36mSkinner: 'Superintendent! Ho, ho, ho! I was just about to climb out of the window to purchase Krusty Burger! Care to join me?'\n\033[34mChalmers: 'I didn't know that you had a sense of humour, Seymour.'\n\033[36mSkinner: 'It's mother's.'\033[34mChalmers: 'I see. Seymour, why is there smoke coming out of your oven, Seymour?'\033[0m",
            "Options": ["Tell the truth","Make up an excuse","Deny the existence of the smoke","Crack a joke"],
            "Move": [20, 21, 22, 23],
        },
        20: {
            "Text": "\033[36mSkinner: The roast is on fire!\n\033[34mChalmers: 'Good lord! And you were climbing out of the window to escape? You know what, Seymour? You're fired!'\033[0m",
            "Lose": "The Seymour is Fired",
        },
        21: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That's from... uh... from the smoked clams we're having!'\n\033[34mChalmers: 'Smoked clams?'\n\033[36mSkinner: 'Yes!'\n\033[0m*Chalmers leaves, and Seymour jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'smoked clams'),
            "Automove": 24,
        },
        22: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That isn't smoke, it's steam! Steam from the steamed clams we're having. Mmmm, steamed clams!'\n\033[0m*Chalmers leaves, and Seymour jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'steamed clams'),
            "Automove": 24,
        },
        23: {
            "Text": "\033[36mSkinner: 'Why do they call it oven when you of in the cold food of out hot eat the food?'\n\033[34mChalmers: '...Yeah.'\033[0m\n*Chalmers leaves, and Skinner jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'some weird roast'),
            "Automove": 24,
        },
        24: {
            "Text": "\033[1mThe Dining Room\033[0m\n+---------+",
            "Script": lambda: time.sleep(0.5),
            "Automove": 25,
        },
        25: {
            "Text": "",
            "Script": lambda: print3(win, str("\033[36mSkinner: 'Superintendent, I hope you're ready for some mouthwatering hamburgers!'\n\033[34mChalmers: 'I thought we were having " + game_state.luncheon + ".'\033[0m")),
            "Options": ["Tell the truth","Make up an excuse"],
            "Move": [26,27],
        },
        26: {
            "Text": "\033[36mSkinner: 'To tell the truth, Superintendent, the roast caught fire, but I just wanted this to be perfect, so I purchased fast food.'\n\033[34mChalmers: 'Look, Seymour, we've worked together for over 30 years. You can tell me when something's wrong, but we have to save your mother and call the fire department. We can reschedule the meeting, how about it, Seymour?'\033[0m",
            "Ending": "Cancelled Luncheon",
        },
    }
    return rooms
##
