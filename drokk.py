 
# drokk.py

import json 
from curses import wrapper
import curses
import webbrowser

FAVORITE_SYMBOL ="♥" 
RETWEET_SYMBOL = "↑"

DEFAULT_COLOR = 0
HANDLE_COLOR = 1
NAME_COLOR = 2
FAVORITE_COLOR = 3
URL_COLOR = 4
HASHTAG_COLOR = 5

def main(stdscr):
    curses.init_pair(HANDLE_COLOR, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(NAME_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(FAVORITE_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(URL_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(HASHTAG_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    stdscr.addstr(0, 0, "drokk\n", curses.A_REVERSE)
    binds = '(r)eload | (q)uit | 0-2 select tweet | open (u)rl of selected tweet'
    stdscr.addstr(curses.LINES -1, 0, binds, curses.A_REVERSE)
    begin_y = 3
    begin_x = 3
    height = curses.LINES -5
    width = curses.COLS -5
    win = curses.newwin(height, width, begin_y, begin_x)

    while True:
        stdscr.refresh()
        c = stdscr.getkey()

        if c == 'q':
            break
        elif c == 'r':
            timeline = read_timeline()
            load_tweets(timeline, win)
        elif c == 'u':
            curses.endwin()
            #webbrowser.open('http://t.co/bfj7zkDJ')
            webbrowser.open(tweet["entities"]["urls"][0]["expanded_url"])
            curses.doupdate()
        elif c in ['0','1','2']:
            tweet = timeline[int(c)]
            stdscr.addstr(1,0,tweet["id_str"], curses.A_REVERSE)

def read_timeline():
    with open("data.json", "r") as data:
        return json.load(data)

def load_tweets(timeline, win):
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
    content = tweet["text"] 
    (y, x) = win.getyx()
    win.addstr(content)
    for url in tweet["entities"]["urls"]:
        win.addstr(y, url["indices"][0], url["url"], curses.color_pair(URL_COLOR) | curses.A_UNDERLINE)

    for url in tweet["entities"]["user_mentions"]:
        win.addstr(y, url["indices"][0], "@" + url["screen_name"], curses.color_pair(HANDLE_COLOR))

    for url in tweet["entities"]["hashtags"]:
        win.addstr(y, url["indices"][0], "#" + url["text"], curses.color_pair(HASHTAG_COLOR))

    win.move(y +1, x)

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

    win.addstr(RETWEET_SYMBOL + " " + str(tweet["retweet_count"]), color)
    
    win.addstr("\n\n")

if __name__ == '__main__':
    wrapper(main)
