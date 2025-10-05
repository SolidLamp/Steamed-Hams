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
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
}
defaultEnding = "You achieved the\n\033[1m|\033[0m\nEnding."
loseText = {
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
    "Fired": "\033[31mFail: You were fired\n\033[0m",
    "The Seymour is Fired": "\033[31mFail: The Seymour is Fired!\n\033[0m",
}
defaultLose = "\n\033[1m|\033[0m"

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
            "Text": "You did not open the door.\n\033[33m*Ding, dong!*\033[0m There goes the doorbell, again.\n\033[34mChalmers: '\033[1mSeymour!\033[0m\033[34m'\033[0m\nOpen it?",
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
            "Text": "\033[36mSkinner: 'You fat-headed buffoon! The directions I gave you were perfectly in order! Plus you've already been here, so you must know the way!'\033[0m\n\033[34mChalmers: '\033[1mSeymour! I have never been more insulted in my life! You're fired!\033[0m\033[34m'\033[0m",
            "Lose": "Fired",
        },
        7: {
            "Text": "*Skinner shuts the door in Chalmer's face*'\033[34mChalmers: \033[1mSEYMOUR!\033[0m\033[34m'",
            "Ending": "Shut Out",
        },
        8: {
            "Text": "\033[36mSkinner: 'Puts-a-bits-a-pits-a-bits-a-pits-a-bits!'\033[0m\n\033[34mChalmers: 'Well, Seymour, I must say, you are an odd fellow.'\033[0m",
            "Script": lambda: time.sleep(0.5),
            "Automove": 11,
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
            "Move": [13, 14, 48, 49]
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
            "Text": "\033[36mSkinner: 'Superintendent! The roast is on fire, I-'\n\033[34mChalmers: 'And you were climbing out of the window to escape?'\n\033[36mSkinner: 'No, I was just-'\n\033[34mChalmers: 'Good lord, Seymour! Aren't you a member of the Springfield Voluntary Fire Department? You haven't alerted me or your mother! We could have been seriously injured!'\n\033[36mSkinner: 'Well, now that you put it like that, I suppose-'\n\033[34mChalmers: That's it, Seymour! \033[1mYou're fired!\033[0m\033[34m'\033[0m",
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
            "Options": ["Tell the truth","Make up an excuse","Make up an excuse","Deny the existence of the smoke","Deny the existence of the smoke","Crack a joke","Crack a joke"],
            "Option1Requirements": lambda: game_state.luncheon != "disguised ruined roast",
            "Option2Requirements": lambda: game_state.luncheon == "disguised ruined roast",
            "Option3Requirements": lambda: game_state.luncheon != "disguised ruined roast",
            "Option4Requirements": lambda: game_state.luncheon == "disguised ruined roast",
            "Option5Requirements": lambda: game_state.luncheon != "disguised ruined roast",
            "Option6Requirements": lambda: game_state.luncheon == "disguised ruined roast",
            "Move": [20, 21, 52, 22, 53, 23, 54],
        },
        19: {
            "Text": "\033[36mSkinner: 'Superintendent! Ho, ho, ho! I was just about to climb out of the window to purchase Krusty Burger! Care to join me?'\n\033[34mChalmers: 'I didn't know that you had a sense of humour, Seymour.'\n\033[36mSkinner: 'It's mother's.'\n\033[34mChalmers: 'I see.'\nChalmers: 'Seymour, why is there smoke coming out of your oven, Seymour?'\033[0m",
            "Options": ["Tell the truth","Make up an excuse","Deny the existence of the smoke","Crack a joke"],
            "Move": [20, 21, 22, 23, ],
        },
        20: {
            "Text": "\033[36mSkinner: The roast is on fire!\n\033[34mChalmers: 'Good lord! And you were climbing out of the window to escape? You know what, Seymour? You're fired!'\033[0m",
            "Lose": "The Seymour is Fired",
        },
        21: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That's from... uh... from the smoked clams we're having!'\n\033[34mChalmers: 'Smoked clams?'\n\033[36mSkinner: 'Yes!'\n\033[0m*Chalmers leaves*\n\033[36mSkinner: 'Phew!'\n\033[0m*Skinner jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'smoked clams'),
            "Automove": 24,
        },
        22: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That isn't smoke, it's steam! Steam from the steamed clams we're having. Mmmm, steamed clams!'\n\033[0m*\n\033[36mSkinner: 'Phew!'\n\033[0m*Skinner jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'steamed clams'),
            "Automove": 24,
        },
        23: {
            "Text": "\033[36mSkinner: 'Why do they call it oven when you of in the cold food of out hot eat the food?'\n\033[34mChalmers: '...Yeah.'\033[0m\n*Chalmers leaves*\n\033[36mSkinner: 'Phew!'\n\033[0m*Skinner jumps through the window to purchase burgers from Krusty Burger*",
            "Script": lambda: setattr(game_state, "luncheon", 'roast'),
            "Automove": 24,
        },
        24: {
            "Text": "\033[1mThe Dining Room\033[0m\n+-------------+",
            "Script": lambda: time.sleep(0.5),
            "Automove": 25,
        },
        25: {
            "Text": "\033[36mSkinner: 'Superintendent, I hope you're ready for some mouthwatering hamburgers!'\n\033[34mChalmers: 'I didn't know we were having hamburgers.'\033[0m",
            "Requirements": lambda: game_state.luncheon == "roast",
            "AlternateText": str("\033[36mSkinner: 'Superintendent, I hope you're ready for some mouthwatering hamburgers!'\n\033[34mChalmers: 'I thought we were having " + game_state.luncheon + ".'\033[0m"),
            "Options": ["Tell the truth","Make up an excuse"],
            "Move": [26,27],
        },
        26: {
            "Text": "\033[36mSkinner: 'To tell the truth, Superintendent, the roast caught fire, but I just wanted this to be perfect, so I purchased fast food.'\n\033[34mChalmers: 'Look, Seymour, we've worked together for over 30 years. You can tell me when something's wrong, but we have to save your mother and call the fire department. We can reschedule the meeting, how about it, Seymour?'\033[0m",
            "Ending": "Cancelled Luncheon",
        },
        27: {
            "Text": "\033[36mSkinner: 'Oh, no, I said steamed hams. That's what I call hamburgers.'\n\033[34mChalmers: 'You call hamburgers steamed hams?'\n\033[36mSkinner: 'Yes. It's a regional dialect.'\n\033[34mChalmers: 'Uh-huh. Uh, what region?'\n\033[36mSkinner: 'Uh...'\033[0m",
            "Options": ["Upstate New York","Russia","Albany","Utica"],
            "Move": [28, 29, 44, 45],
        },
        28: {
            "Text": "\033[36mSkinner: 'Upstate New York.'\n\033[34mChalmers: 'Really? Well I'm from Utica and I've never heard anyone use the phrase steamed hams.'\033[0m",
            "Options": ["Specify a more specific region","Escape the conversation"],
            "Move": [31, 35],
        },
        29: {
            "Text": "\033[36mSkinner: 'Russia.'\n\033[34mChalmers: 'Look, Seymour, I know your family history - you're not from Russia.'\n\033[36mSkinner: 'Oh. Uh...'\033[0m",
            "Options": ["Play it off as a joke","Double down"],
            "Move": [30, 47],
        },
        30: {
            "Text": "\033[36mSkinner: 'Ho, ho, ho, no!'\n\033[36mSkinner: 'I was just 'pulling your thread', as they say.'\n\033[36mSkinner: 'I'm really from upstate New York.'\n\033[34mChalmers: 'Really? Well I'm from Utica and I've never heard anyone use the phrase steamed hams.'\033[0m",
            "Options": ["Specify a different region","Escape the conversation"],
            "Move": [31,35],
        },
        31: {
            "Text": "\033[36mSkinner: 'Oh, not in Utica, no. It's an Albany expression.'\n\033[34mChalmers: 'I see.'\nChalmers: You know, these hamburgers are quite similar to the ones they have at Krusty Burger.'\033[0m",
            "Options": ["Tell the truth","'Old Family Recipe'"],
            "Move": [32,33],
        },
        32: {
            "Text": "\033[36mSkinner: 'Well, that's because they are.'\n\033[34mChalmers: 'What?! You're telling me that you bought Krusty Burgers and served them to me as your own- \033[1mGOOD LORD!\033[0m\033[34m What is happening in there?!'\033[0m",
            "Options": ["Fire","Roboticiser","Aurora Borealis"],
            "Move": [36,37,38],
        },
        33: {
            "Text": "\033[36mSkinner: 'Ho, ho, ho, no! Patented Skinner Burgers. Old family recipe!'\n\033[34mChalmers: 'For steamed hams?'\n\033[36mSkinner: 'Yes.'\n\033[34mChalmers: 'Yes, and you call them steamed hams, despite the fact they are obviously grilled.'\033[0m",
            "Options": ["Respond with confidence","Escape the conversation"],
            "Move": [34,35],
        },
        34: {
            "Text": "\033[36mSkinner: 'Y- Uh.. Yes!'\n\033[34mChalmers: 'I see'.\nChalmers: 'Well, I should probably be g- \033[1m GOOD LORD! \033[0m\033[34m What is happening in there?!'\033[0m",
            "Options": ["Fire","Roboticiser","Aurora Borealis"],
            "Move": [36,37,38],
        },
        35: {
            "Text": "\033[36mSkinner: 'Y- Uh.. you know, the... One thing I should... excuse me for one second.'\n\033[34mChalmers: 'Of course.'\033[0m*Skinner enters the kitchen for a couple seconds before leaving again, and returning.*\n\033[36mSkinner: *BIG YAWN* 'Well, that was wonderful. A good time was had by all. I'm pooped.\n\033[34mChalmers: 'Yes, I should be- \033[1m GOOD LORD! \033[0m What is happening in there?!'\033[0m",
            "Options": ["Fire","Roboticiser","Aurora Borealis"],
            "Move": [36,37,38],
        },
        36: {
            "Text": "\033[36mSkinner: 'The kitchen in on fire!'\n\033[34mChalmers: '\033[1mGood lord!\033[34m We have to save your mother and call the fire department!'\n\033[0m*Through Skinner and Chalmer's swift actions, Agnes is saved and the fire department arrive to extinguish Skinner's house*\n\033[34mChalmers: 'Well, Seymour, that certainly was an unforgettable luncheon.'\033[0m",
            "Ending": "Unforgettable Luncheon, but not in a good way",
        },
        37: {
            "Text": "\033[36mSkinner: 'Uhh... Roboticiser.'\n\033[34mChalmers: 'Wha-'\n\033[0m*Robotnik steps out of the kitchen, causing Skinner to die of a heart attack*",
            "Ending": "Saturday Morning",
        },
        38: {
            "Text": "\033[36mSkinner: 'Aurora Borealis.'\n\033[34mChalmers: '\033[1mA-Aurora Borealis?!\033[0m\033[34m'\nChalmers: '\033[1mAt this time of year,\033[0m\033[34m'\nChalmers: '\033[1mAt this time of day,\033[0m\033[34m'\nChalmers: '\033[1mIn this part of the country,\033[0m\033[34m'\nChalmers: '\033[1mLocalised entirely within your kitchen?!\033[0m\033[34m'\033[0m",
            "Options": ["Yes","No"],
            "Move": [40,39],
        },
        39: {
            "Text": "\033[36mSkinner: 'No, I was joking. It is actually a fire. It would be wise to contact the local authorities.'\n\033[34mChalmers: 'Good lord, you're joking when there's a fire?! For your clear show of negligence, I can't trust you to take care of a school full of children, you're fired!'\033[0m",
            "Lose": "Fired",
        },
        40: {
            "Text": "\033[36mSkinner: 'Yes.'\n\033[34mChalmers: May I see it?'\033[0m",
            "Options": ["Yes","No"],
            "Move": [41,43],
        },
        41: {
            "Text": "\033[36mSkinner: Yes!\n\033[0m*Skinner and Chalmers enter the kitchen, viewing The Northern Lights up close.*",
            "Automove": 42
        },
        42: {
            "Text": "\033[34mChalmers: 'Well, Seymour, I must say, that was certainly an unforgettable luncheon.'\033[0m",
            "Ending": "Unforgettable Luncheon"
        },
        43: {
            "Text": "\033[36mSkinner: 'No.'\n\033[0m*Skinner and Chalmers exit the house*\n\033[35mAgnes: '\033[1mSeymour! The house is on fire!\033[0m\033[35m'\n\033[36mSkinner: 'No, mother, it's just the Northern Lights!'\n\033[34mChalmers: 'Well, Seymour, you are an odd fellow, but I must say, you steam a good ham.'\n\033[35mAgnes: '\033[1mHelp! HELP!!!\033[0m\033[35m'\n\033[0m*Skinner shows Chalmers a thumbs up and Chalmers heads home*\033[0m",
            "Ending": "Homeless",
        },
        44: {
            "Text": "\033[36mSkinner: 'It's an Albany expression.'\n\033[34mChalmers: 'I see.'\nChalmers: You know, these hamburgers are quite similar to the ones they have at Krusty Burger.'\033[0m",
            "Options": ["Tell the truth","'Old Family Recipe'"],
            "Move": [32,33],
        },
        45: {
            "Text": "\033[36mSkinner: 'It's a Utica expression'\n\033[34mChalmers: 'Really? Well, I'm from- Wait, did you just say Utica?'\n\033[36mSkinner: 'Uh... Yes! '\n\033[34mChalmers: 'In all my years of working with you, Seymour, I had no idea that you were from Utica. So, where did you grow up in Utica?'\n\033[36mSkinner: 'Well...'\033[0m",
            "Automove": 46,
        },
        46: {
            "Text": "*After a long talk and meal...*\n\033[34mChalmers: 'Well, Seymour, that was certainly an interesting meal. Perhaps we got off on the wrong foot. I really must be going now, but I will certainly be looking towards our next meeting!",
            "Ending": "Utica"
        },
        47: {
            "Text": "\033[36mSkinner: 'Actually, my family history does trace back to Russia. You see, my great-great-great-great-great grandmother and grandfather were actually, uh, Armenian, in the Russian Empire. I, uh, think they left sometime in the, uh, 18th century. They've passed down many heirlooms including a recipe book which has a recipe for steamed hams, so that's why I call it that.'\n\033[34mChalmers: 'Well, I wouldn't say they were Russian - Armenia was quite a separate region from the Russian Empire; you can't really reduce an ethnic group to the nationality of their country - we can see that here even in America.'\n\033[36mSkinner: 'Yes, well, I suppose I can agree with that, but I wouldn't have expected you to know so much about Armenia, and I didn't say they were Russian.'\n\033[34mChalmers: 'But your family is really from Armenia? That's really interesting. Can I ask more about them?'\n\033[36mSkinner: 'Of course, Superintendent, but I can't guarantee I'll know everything - it's a long time ago.'\033[0m",
            "Script": lambda: time.sleep(1),
            "Automove": 46,
        },
        48: {
            "Text": "\033[36mSkinner: 'But what if I were to serve ruined roast and disguise it as mouthwatering hamburgers? [chuckles] Delightfully devilish, Seymour.'\033[0m\n*Chalmers enters the kitchen*\n\033[34mChalmers: 'SEEEEEYMOOUUURRR!!!'\033[0m",
            "Script": lambda: setattr(game_state, "luncheon", 'disguised ruined roast'),
            "Options": ["Tell the truth","Opening a window","Random activity","Skydiving out of the window"],
            "Move": [15, 16, 18, 17]
        },
        49: {
            "Text": "\033[36mSkinner: 'But what if I were to serve ruined roast as a prank? [chuckles] Delightfully devilish, Seymour.'\033[0m\n*Chalmers enters the kitchen*\n\033[34mChalmers: 'SEEEEEYMOOUUURRR!!!'\033[0m",
            "Options": ["Tell him about the roast", "Tell him to prepare for the unforgettable luncheon"],
            "Move": [50, 51]
        },
        50: {
            "Text": "\033[36mSkinner: 'Superintendent! I hope you're prepared for ruined roast!'\033[0m\n\033[34mChalmers: 'R-ruined roast?'\n\033[36mSkinner: 'Yes!'\n\033[34mChalmers: 'Perhaps we should have this lunch at another time, Seymour.'\033[0m",
            "Ending": "Idiot"
        },
        51: {
            "Text": "\033[36mSkinner: 'Superintendent! I hope you're prepared for an unforgettable luncheon!'\n\033[34mChalmers: 'Why is there smoke coming out of your oven, Seymour?'\033[0m",
            "Script": lambda: setattr(game_state, "luncheon", 'ruined roast'),
            "Options": ["Tell the truth","Make up an excuse","Deny the existence of the smoke","Crack a joke"],
            "Move": [20, 52, 53, 54],
        },
        52: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That's from... uh... from the smoked clams we're having!'\n\033[34mChalmers: 'Smoked clams?'\n\033[36mSkinner: 'Yes!'\n\033[0m*Chalmers leaves*\n\033[36mSkinner: 'Phew!'\033[0m",
            "Automove": 55,
        },
        53: {
            "Text": "\033[36mSkinner: 'Uh... ooh! That isn't smoke, it's steam! Steam from the steamed clams we're having. Mmmm, steamed clams!'\n\033[0m*Chalmers leaves*\n\033[36mSkinner: 'Phew!'\033[0m",
            "Automove": 55,
        },
        54: {
            "Text": "\033[36mSkinner: 'Why do they call it oven when you of in the cold food of out hot eat the food?'\n\033[34mChalmers: '...Yeah.'\033[0m\n*Chalmers leaves*\n\033[36mSkinner: 'Phew!'\033[0m",
            "Automove": 55,
        },
        55: {
            "Text": "\033[1mThe Dining Room\033[0m\n+-------------+",
            "Script": lambda: time.sleep(0.5),
            "Automove": 56,
        },
        56: {
            "Text": "\033[36mSkinner: 'Superintendent, I hope you're ready for some mouthwatering hamburgers!'\n\033[34mChalmers: 'I didn't know we were having hamburgers.'\033[0m",
            "Requirements": lambda: game_state.luncheon == "disguised ruined roast",
            "AlternateText": "\033[36mSkinner: 'Superintendent, I hope you're ready for some mouthwatering hamburgers!'\n\033[34mChalmers: 'I though- \033[1mGOOD LORD!\033[0m\033[34m What in the world is that?'\033[0m",
            "Options": ["Tell the truth","Make up an excuse","Present the unforgettable luncheon"],
            "Option1Requirements": lambda: game_state.luncheon == "disguised ruined roast",
            "Option2Requirements": lambda: game_state.luncheon == "ruined roast",
            "Move": [57,27,58],
        },
        57: {
            "Text": "\033[36mSkinner: 'To tell the truth, Superintendent, the roast caught fire, but I just wanted this to be perfect, so I attempted to disguise it.'\n\033[34mChalmers: 'Look, Seymour, we've worked together for over 30 years. You can tell me when something's wrong. Is the oven off completely? We should run a check to make sure nothing is damaged. We can always reschedule the meeting, how about it, Seymour?'\033[0m",
            "Ending": "Cancelled Luncheon",
        },
        58: {
            "Text": "\033[36mSkinner: 'Superintendent Chalmers! It's my finest meal yet! A truly unforgettable luncheon!'\n\033[34mChalmers: 'What have you done? What... Keep that away from me! Look, just, whatever, I'll give more funding to the school - just keep that \033[1mthing\033[0m\033[34m away from me!'\033[0m",
            "Ending": "Funding",
        },
    }
    return rooms
##
