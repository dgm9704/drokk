 
# drokk.py

import json 
from curses import wrapper
import curses

FAVORITE_SYMBOL ="♥" 
RETWEET_SYMBOL = "↑"

DEFAULT_COLOR = 0
HANDLE_COLOR = 1
NAME_COLOR = 2
FAVORITE_COLOR = 3

def main(stdscr):
    curses.init_pair(HANDLE_COLOR, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(NAME_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(FAVORITE_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
    
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
    

def output_tweet(tweet, win):
    write_header(tweet, win)
    write_content(tweet, win)
    write_footer(tweet, win)

def write_header(tweet, win):
    handle = "@" + tweet["user"]["screen_name"] 
    win.addstr(handle, curses.color_pair(HANDLE_COLOR))
    name = tweet["user"]["name"] 
    win.addstr(" (" + name + ")\n", curses.color_pair(NAME_COLOR))

def write_content(tweet, win):
    content = tweet["text"] + "\n"
    win.addstr(content)

def write_footer(tweet, win):
    if tweet["favorited"] == True:
        color = curses.color_pair(FAVORITE_COLOR)
    else:
        color = curses.color_pair(DEFAULT_COLOR)

    win.addstr(FAVORITE_SYMBOL + " " + str(tweet["user"]["favourites_count"]), color)

    win.addstr("\t\t")
    if tweet["retweeted"] == True:
        color = curses.color_pair(FAVORITE_COLOR)
    else:
        color = curses.color_pair(DEFAULT_COLOR)

    win.addstr(FAVORITE_SYMBOL + " " + str(tweet["retweet_count"]), color)
    
    win.addstr("\n\n")

if __name__ == '__main__':
    wrapper(main)
