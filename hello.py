 
# hello.py

import json
from curses import wrapper
import curses

HANDLE_COLOR = 1
NAME_COLOR = 2

def main(stdscr):
    curses.init_pair(HANDLE_COLOR,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(NAME_COLOR,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    
    stdscr.addstr(0,0,"drokk\n", curses.A_REVERSE)
    stdscr.refresh()

    with open("data.json","r") as data:
        timeline = json.load(data)

    for tweet in timeline:
        output_tweet(tweet,stdscr)
       
    stdscr.refresh()
    stdscr.getch()

def output_tweet(tweet,win):
    handle = "@" + tweet["user"]["screen_name"] 
    win.addstr(handle,curses.color_pair(HANDLE_COLOR))
    win.addstr("\t")
    name = tweet["user"]["name"] 
    win.addstr(" (" + name + ")\n", curses.color_pair(NAME_COLOR))
    content = tweet["text"] + "\n"
    win.addstr(content)
    win.addstr("\n")


if __name__ == '__main__':
    wrapper(main)
