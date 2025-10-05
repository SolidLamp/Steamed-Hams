import time

def print2(a):
    for i in a:
        print(i, end="", flush=True)
        time.sleep(0.01)
    print()

def option(a):
    print()
    for i, options in enumerate(a, start=1):
        print2(f"{i}. {options}")
    query=input(">>> ")
    print()
    return(query)




def ending(a):
    print()
    print()
    print()
    time.sleep(0.25)
    print("You achieved the:")
    time.sleep(0.25)
    print()
    print("\033[1m" + a + "\033[0m")
    time.sleep(0.25)
    print()
    print("Ending.")
    time.sleep(0.5)
    print()
    print()
    print()
    print("Try again?")

# The Game

def intro():
    print2("\033[1m" + "Steamed Hams: The Game, Plus! Edition" + "\033[0m")
    print2("Use the numbers to choose options")
    query = option(["Begin"])
    if query == "1":
        gameLoop()
    else:
        exit()

def gameLoop():
    print2("[Ding, dong!]")
    print2("It's the doorbell.")
    print2("Open it?")
    query = option(["Yes","No"])
    if query == "1":
        action1()
    elif query == "2":
        ending("I haven't coded this yet")
    else:
        gameLoop()
    query = option(["Yes","No"])
    if query == "1":
        gameLoop()
    elif query == "2":
        exit()
    else:
        exit()
    

def action1():
    print2("Chalmers: Well, Seymour, I made it, despite your directions.")
    query = option(["Aggressive and rude insult","Overly friendly greeting","Shut the door","Beatbox","[Say nothing]"])
    if query == "1":
        action2()
    elif query == "2":
        print2("Skinner: Ah, Superintendent Chalmers, welcome! I hope you're prepared for an unforgettable luncheon!")
        action3()
    elif query == "3":
        ending("I haven't coded this yet")
    elif query == "4":
        ending("I haven't coded this yet")
    elif query == "5":
        time.sleep(0.5)
        action3()
    else:
        action1()
    

def action2():
    print2("Skinner: You fat-headed buffoon! The directions I gave you were perfectly in order! Plus you've already been here, so you must know the way!")
    print2("Chalmers: Seymour! I have never been more insulted in my life! You're fired!")
    ending("Fired")

def action3():
    print2("Chalmers: Yeah.")
    print2("[Skinner enters the kitchen, soon realising that his roast is ruined.]")
    print2("Skinner: Oh, egads! My roast is ruined!")
    query=option(["Tell the truth","Lie and purchase fast food","Serve ruined roast","Serve the roast anyway, and ignore the fact that it is ruined"])
    if query == "1":
        action4()
    elif query == "2":
        action5()
    elif query == "3":
        ending("I haven't coded this yet")
    elif query == "4":
        ending("I haven't coded this yet")
    else:
        action3()

def action4():
    print2("Skinner: Superintendent! The roast is on fire!")
    print2("Chalmers: Good lord! We have to put it out!")
    print2("Skinner and Chalmers extinguish the fire before any harm occurs.")
    print2("Chalmers: Well, Seymour, we saved the house, but the roast is unrecoverable.")
    print2("Skinner: Well, there's a Krusty Burger just over there. We could have that.")
    print2("Chalmers: Krusty Burger. Yes, I do enjoy the food there. I suppose we could.")
    print2("[Skinner and Chalmers consume the Krusty Burgers.]")
    print2("Chalmers: Well Seymour, that was quite enjoyable, but I must go now. I will see you at work tomorrow.")
    ending("Honest Abe")

def action5():
        print2("Skinner: But what if I were to purchase fast food and disguise it as my own cooking? [chuckles] Delightfully devilish, Seymour.")
        print2("[Chalmers enters the kitchen, viewing Skinner attempting to escape out of the window]")
        print2("Chalmers: SEEEEEYMOOUUURRR!!!")
        query=option(["Tell the truth","Opening a window","Stretching your calves on the windowsill","Skydiving out of the window","Tell the truth, but play it off as a joke"])
        if query == "1":
            action6()
        elif query == "2":
            action7()
        elif query == "3":
            action9()
        elif query == "4":
            action8()
        elif query == "5":
            ending("I haven't coded this yet")
        else:
            action5()

def action6():
    print2("Skinner: Superintendent! The roast is on fire, I-")
    print2("Chalmers: And you were climbing out of the window to escape?")
    print2("Skinner: No, I was just-")
    print2("Chalmers: Good lord, Seymour! Aren't you a member of the Springfield Voluntary Fire Department? You haven't alerted me or your mother! We could have been seriously injured!")
    print2("Skinner: Well, now that you put it like that, I think-")
    print2("Chalmers: That's it, Seymour! You're fired!")
    ending("Fired")

def action7():
    print2("Skinner: Superintendent! I was just opening a window to let the smoke out.")
    print2("Chalmers: Smoke? What smoke? Good lord, the oven is on fire!")
    print2("Skinner: Uh, I meant that I was, uh-")
    print2("Chalmers: Seymour, you were clearly climbing out of the window to escape!")
    print2("Skinner: Ooh, uh, I was, uh, just, um-")
    print2("Chalmers: That's it, Seymour! I'm firing you for lack of safety and neglect!")
    ending("Fired")

def action8():
    print2("Skinner: Superintendent! I was just skydiving out of the window!")
    print2("Chalmers: What?")
    ending("What")

def action9():
    print2("Skinner: Superintendent! I was just, uh, just stretching my calves on the windowsill. Isometric exercise! Care to join me?")
    print2("Chalmers: Why is there smoke coming out of your oven, Seymour?")
    query=option(["Tell the truth","Make up an excuse"])
    if query == "1":
        action10()
    elif query == "2":
        action11()
    else:
        action9()
    
def action10():
    print2("Skinner: The roast is on fire!")
    print2("Chalmers: Good lord! And you were climbing out of the window to escape? You know what, Seymour, you're fired!")
    #ending("The Seymour is fired!")
    ending("Fired")

def action11():
    print2("Skinner: Uh... ooh! That isn't smoke, it's steam! Steam from the steamed clams we're having. Mmmm, steamed clams!")
    print2("[Chalmers leaves, and Seymour climbs out the window to purchase Krusty Burger]")
    print2("Skinner: Superintendent, I hope you're ready for some mouthwatering hamburgers.")
    print2("Chalmers: I thought we were having steamed clams.")
    query=option(["Tell the truth","Make up an excuse"])
    if query == "1":
        action12()
    elif query == "2":
        action13()
    else:
        action11()

def action12():
    print2("Skinner: To tell the truth, Superintendent, the roast caught fire, but I just wanted this to be perfect, so I purchased fast food.")
    print2("Chalmers: Look, Seymour, we've worked together for over 30 years. You can tell me when something's wrong, but we have to save your mother and call the fire department. We can reschedule the meeting, how about it, Seymour?")
    ending("Cancelled Luncheon")

def action13():
    print2("Skinner: Oh no, I said steamed hams. That's what I call hamburgers.")
    print2("Chalmers: You call hamburgers steamed hams?")
    print2("Skinner: Yes. It's a regional dialect.")
    print2("Chalmers: Uh-huh. Eh, what region?")
    print2("Skinner: Uh...")
    query=option(["Upstate New York","Russia","Albany","Utica"])
    if query == "1":
        action14()
    elif query == "2":
        action15()
    elif query == "3":
        ending("I haven't coded this yet")
    elif query == "4":
        ending("I haven't coded this yet")
    else:
        action13()

def action14():
    print2("Skinner: Upstate New York.")
    print2("Chalmers: Really? Well I'm from Utica and I've never heard anyone use the phrase steamed hams.")
    query=option(["Specify a more specific region","Escape the conversation"])
    if query == "1":
        action17()
    elif query == "2":
        action21()
    else:
        action14()



def action15():
    print2("Skinner: Russia.")
    print2("Chalmers: Look, Seymour, I know your family history - you're not from Russia.")
    print2("Skinner: Oh. Uh...")
    query=option(["Play it off as a joke","Double down"])
    if query == "1":
        action16()
    elif query == "2":
        ending("I haven't coded this yet")

def action16():
    print2("Skinner: Ho, ho, ho, no!")
    print2("Skinner: I was just 'pulling your thread', as they say.")
    print2("Skinner: I'm really from upstate New York.")
    print2("Chalmers: Really? Well I'm from Utica and I've never heard anyone use the phrase steamed hams.")
    query=option(["Specify a different region","Escape the conversation"])
    if query == "1":
        action17()
    elif query == "2":
        action21()
    else:
        action14()

def action17():
    print2("Skinner: Oh, not in Utica, no. It's an Albany expression.")
    print2("Chalmers: I see.")
    print2("Chalmers: You know, these hamburgers are quite similar to the ones they have at Krusty Burger.")
    query=option(["Tell the truth","'Old Family Recipe'"])
    if query == "1":
        action18()
    elif query == "2":
        action19()
    else:
        action17()    

def action18():
    print2("Skinner: Well, that's because they are.")
    print2("Chalmers: What?! You're telling me that you bought Krusty Burgers and served them to me as your own- \033[1m GOOD LORD! \033[0m What is happening in there?!")
    query=option(["Fire","Roboticiser","Aurora Borealis"])
    if query == "1":
        action22()
    elif query == "2":
        action23()
    elif query == "3":
        action24()
    else:
        action18()

def action19():
    print2("Skinner: Hohoho, no! Patented Skinner Burgers. Old family recipe!")
    print2("Chalmers: For steamed hams?")
    print2("Skinner: Yes.")
    print2("Chalmers: Yes, and you call them steamed hams, despite the fact they are obviously grilled.")
    query=option(["Respond with confidence","Escape the conversation"])
    if query == "1":
        action20()
    elif query == "2":
        action21()
    else:
        action19()
    
def action20():
    print2("Skinner: Y- Uh.. Yes!")
    time.sleep(1)
    print2("Chalmers: I see.")
    time.sleep(1)
    print2("Chalmers: Well, I should probably be g- \033[1m GOOD LORD! \033[0m What is happening in there?!")
    query=option(["Fire","Roboticiser","Aurora Borealis"])
    if query == "1":
        action22()
    elif query == "2":
        action23()
    elif query == "3":
        action24()
    else:
        action20()
        

def action21():
    print2("Skinner: Y- Uh.. you know, the... One thing I should... excuse me for one second.")
    print2("Chalmers: Of course.")
    print2("[Skinner enters the kitchen for a couple seconds before leaving again, and returning.")
    print2("Skinner: [BIG YAWN] Well, that was wonderful. A good time was had by all. I'm pooped.")
    print2("Chalmers: Yes, I should be- \033[1m GOOD LORD! \033[0m What is happening in there?!")
    query=option(["Fire","Roboticiser","Aurora Borealis"])
    if query == "1":
        action22()
    elif query == "2":
        action23()
    elif query == "3":
        action24()
    else:
        action21()

def action22():
    print2("Skinner: The kitchen in on fire!")
    print2("Chalmers: Good lord! We have to save your mother and call the fire department!")
    print2("[Agnes is saved and the fire department arrive to extinguish Skinner's house]")
    print2("Chalmers: Well, Seymour, that was an unforgettable luncheon.")
    ending("Unforgettable Luncheon, but not in a good way")

def action23():
    print2("Skinner: Uhh... Roboticiser.")
    print2("Chalmers: Wha-")
    print2("[Robotnik steps out of the kitchen, causing Skinner to die of a heart attack]")
    ending("Saturday Morning")

def action24():
    print2("Skinner: Aurora Borealis.")
    print2("Chalmers: \033[1m A-Aurora Borealis?!")
    print2("Chalmers: At this time of year,")
    print2("Chalmers: At this time of day,")
    print2("Chalmers: In this part of the country,")
    print2("Chalmers: Localised entirely within your kitchen?! \033[0m")
    query=option(["Yes","No"])
    if query == "1":
        action26()
    elif query == "2":
        action25()
    else:
        action24()

def action25():
    print2("Skinner: No; I was joking. It is actually a fire. It would be wise to contact the local authorities.")
    print2("Chalmers: Good lord, you're joking when there's a fire?! For your clear show of negligence, you're fired!")
    ending("Fired")

def action26():
    print2("Skinner: Yes.")
    time.sleep(0.5)
    print2("Chalmers: May I see it?")
    query=option(["Yes","No"])
    if query == "1":
        action27()
    elif query == "2":
        action28()
    else:
        action26()

def action27():
    print2("Skinner: Yes.")
    print2("[Skinner and Chalmers enter the kitchen, viewing The Northern Lights up close.]")
    time.sleep(0.25)
    print2("Chalmers: Well, Seymour, that was an unforgettable luncheon.")
    ending("Unforgettable Luncheon")

def action28():
    print2("Skinner: No.")
    print2("[Skinner and Chalmers exit the house]")
    print2("Agnes: Seymour! The house is on fire!")
    print2("Skinner: No, mother, it's just the Northern Lights.")
    print2("Chalmers: Well, Seymour, you are an odd fellow, but I must say, you steam a good ham.")
    print2("Agnes: Help! HELP!!!")
    print2("[Skinner shows Chalmers a thumbs up and Chalmers heads home")
    ending("Homeless")

intro()
exit()

#Achievements: Vetaran (get all original endings in Skinner's path), Newbie (get all Plus! endings in Skinner's path), Seymour Butts (get all of Skinner's endings), the Superintendent's Gonna Need His Medication (get all of Chalmer's endings), Steamed Hams (Get the Canon Ending), Champion (Get the most points possible.), 
