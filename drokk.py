 
# drokk.py

import json 
from curses import wrapper
import curses

HANDLE_COLOR = 1
NAME_COLOR = 2

def main(stdscr):
    curses.init_pair(HANDLE_COLOR, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(NAME_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    stdscr.addstr(0, 0, "drokk\n", curses.A_REVERSE)
    binds = '(r)eload (q)uit'
    stdscr.addstr(curses.LINES -1, 0, binds, curses.A_REVERSE)
    begin_y = 3
    begin_x = 3
    height = curses.LINES -5
    width = curses.COLS -5
    win = curses.newwin(height, width, begin_y, begin_x)

    while True:
        stdscr.refresh()
        c = stdscr.getch()

        if c == ord('q'):
            break
        elif c == ord('r'):
            load_tweets(win)

def load_tweets(win):
    with open("data.json", "r") as data:
        timeline = json.load(data)

    win.erase()

    for tweet in timeline:
        output_tweet(tweet,win)
        win.refresh()
    

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
