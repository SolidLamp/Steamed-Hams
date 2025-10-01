import curses
import os
import time
#import math
import sys

value = 0

#def uutime(win):
#while 1:
#win.clear()
#win.addstr(str(math.floor(time.time())))
#win.refresh()

def colorsetup(win):
  curses.start_color() #curses.A_NORMAL | curses.A_BOLD
  curses.init_pair(31, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(32, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(33, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(35, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
  curses.init_pair(36, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(37, curses.COLOR_WHITE, curses.COLOR_BLACK)
  curses.init_pair(41, curses.COLOR_BLACK, curses.COLOR_RED)
  curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_GREEN)
  curses.init_pair(43, curses.COLOR_BLACK, curses.COLOR_YELLOW)
  curses.init_pair(44, curses.COLOR_BLACK, curses.COLOR_BLUE)
  curses.init_pair(45, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
  curses.init_pair(46, curses.COLOR_BLACK, curses.COLOR_CYAN)
  curses.init_pair(47, curses.COLOR_BLACK, curses.COLOR_WHITE)

def print3(win, text, colorcode=0, delay=0.01, pauseAtNewline=0.0):
  #colorsetup(win)
  i = 0
  ansi = int(colorcode)
  while i < len(text):
    char = text[i]
    if char == "\n":
      newline(win)
      time.sleep(pauseAtNewline)
    elif char == "\033": #\033[xm \033[xxm
      if text[i+1] == "[" and text[i+3].isdigit():
        ansi = int(text[i+2] + text[i+3])
        i += 4
      elif text[i+1] == "[" and text[i+3] == "m":
        if text[i+2] == "0":
          win.addstr("", curses.A_NORMAL)
          ansi = 0
        elif text[i+2] == "1":
          win.addstr("", curses.A_BOLD)
        i += 3
    else:
      win.addstr(char, curses.color_pair(ansi))
      win.refresh()
      time.sleep(delay)
    i += 1


def newline(win):
  max_y, max_x = win.getmaxyx()
  y, x = win.getyx()
  y += 1
  x = 0
  if y >= max_y:
    win.scroll()
    y = max_y - 1
  if y >= max_y - 1:
    win.move(max_y - 1, x)
  else:
    win.move(y, x)
  win.refresh()


def option(win, text, options):
  value = 0
  win.nodelay(False)
  while (1):
    win.clear()
    win.move(0, 0)
    curses.curs_set(0)
    win.scrollok(True)
    print3(win, text, 0, 0)
    win.refresh()
    for option in options:
      newline(win)
      win.addstr(" ")
      if options.index(option) == value:
        win.addstr("> ")
        win.addstr(str(option), curses.A_STANDOUT)
      else:
        win.addstr(str(option))
    #win.getch()
    try:
      key = win.getkey()
    except Exception:
      key = "KEY_UP"
    if key == os.linesep:
      return (value)
    if key == "KEY_UP" and value > 0:
      value -= 1
    elif key == "KEY_DOWN" and value < (len(options) - 1):
      value += 1
    elif key == "q":
      return("q")
      print3(win, "Are you sure you want to quit?", 0, 0)
      sys.exit()
    win.refresh()


#def main(win):
#  #win.nodelay(False)
#  key = ""
#  while 1:
#    try:
#      key = win.getkey()
#      win.clear()
#      win.addstr("\n")
#      win.addstr("Detected key:")
#      win.addstr(str(key))
#      value = option(win, key, ["Option 0","Option 1"])
#      if key == os.linesep:
#        return(value)
#    except Exception:
#      pass

#value = curses.wrapper(main)
#print(value)
