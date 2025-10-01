import sys
import tui
from shm import gameLoop
try:
    import curses
except ImportError as e:
    print(f"The curses module was not found. If you are running Windows, please install windows-curses with pip.\nError: {e}")
    sys.exit(1)

def main(win):
    win.clear()
    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    win.addstr(r"""

 ##  #                         #     #  #
#   ###  ##  ##  #####   ##    #     #  #  ## #####   ###  #
 #   #  # # # #  # ## # # #  ###     #### # # # ## # ##
  #  #  ##  # #  # ## # ##   # #     #  # # # # ## #   ##  #
##   ##  ## #### # ## #  ##  ###     #  # ### # ## # ###

##### #             ###
  #   #     ##     #      ##  #####   ##
  #   ###  # #     #  ## # #  # ## # # #    @-+-+-+-+-@  @-+-+-+-+-+-+-@
  #   #  # ##      #   # # #  # ## # ##     |P|l|u|s|!|  |E|d|i|t|i|o|n|
  #   #  #  ##      ###  #### # ## #  ##    @-+-+-+-+-@  @-+-+-+-+-+-+-@
                                                       """)
    query = tui.option(win, "\033[36m\n ##  #                         #     #  #\n#   ###  ##  ##  #####   ##    #     #  #  ## #####   ###  #\n #   #  # # # #  # ## # # #  ###     #### # # # ## # ##\n  #  #  ##  # #  # ## # ##   # #     #  # # # # ## #   ##  #\n##   ##  ## #### # ## #  ##  ###     #  # ### # ## # ###\n\n##### #             ###\n  #   #     ##     #      ##  #####   ##\n  #   ###  # #     #  ## # #  # ## # # #    @-+-+-+-+-@  @-+-+-+-+-+-+-@\n  #   #  # ##      #   # # #  # ## # ##     |P|l|u|s|!|  |E|d|i|t|i|o|n|\n  #   #  #  ##      ###  #### # ## #  ##    @-+-+-+-+-@  @-+-+-+-+-+-+-@\033[0m",["Begin", "Skip Intro", "Quit"])
    win.clear()
    win.move(0,0)
    curses.curs_set(0)
    loop = 0
    if query == 0:
        tui.print3(win, "You are a travelling merchant, approaching a new village to sell your wares in another region.\nAs you approach the village, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just on the outskirts of our little village.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them.\nAny that resided within the main parts of the village limits last night have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the village with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?'\033[0m he continues, \033[33m'There's an old legend that if all seems to disappear overnight, then it marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a golden idol.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the main limits of the village.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m\nThe man leaves.\nPress any key to continue...", 0, 0.02)
        win.refresh()
        win.getch()
        loop = gameLoop(win, 1)
    if query == 1:
        loop = gameLoop(win, 2)
    else:
        sys.exit()
    while loop == 0:
        loop = gameLoop(win)
        win.addstr(str(loop))

def title():
    print("If you can read this, the game is not displaying. The most likely scenario is that you have closed the game.")
    while 1:
        curses.wrapper(main)
