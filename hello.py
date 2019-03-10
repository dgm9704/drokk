 
# hello.py

import json
from curses import wrapper
import curses

def main(stdscr):
    HANDLE_COLOR = 1
    NAME_COLOR = 2
    curses.init_pair(HANDLE_COLOR,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(NAME_COLOR,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    stdscr.addstr(0,0,"drokk\n", curses.A_REVERSE)
    stdscr.refresh()

    with open("data.json","r") as data:
        timeline = json.load(data)

    for tweet in timeline:
        handle = "@" + tweet["user"]["screen_name"] 
        stdscr.addstr(handle,curses.color_pair(HANDLE_COLOR))
        stdscr.addstr("\t")
        name = tweet["user"]["name"] 
        stdscr.addstr(" (" + name + ")\n", curses.color_pair(NAME_COLOR))
        content = tweet["text"] + "\n"
        stdscr.addstr(content)
        stdscr.addstr("\n")
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    wrapper(main)
