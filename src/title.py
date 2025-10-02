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
        win.refresh()
        loop = gameLoop(win, 1)
    if query == 1:
        loop = gameLoop(win, 25)
    else:
        sys.exit()
    while loop == 0:
        loop = gameLoop(win)
        win.addstr(str(loop))

def title():
    print("If you can read this, the game is not displaying. The most likely scenario is that you have closed the game.")
    while 1:
        curses.wrapper(main)
