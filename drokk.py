 
# drokk.py

import json 
from curses import wrapper
import curses
import webbrowser
import math
import subprocess

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
    
    begin_y = 3
    begin_x = 3
    height = curses.LINES -5
    width = curses.COLS -5
    win = curses.newwin(height, width, begin_y, begin_x)
    selection = -1 
    pages = 0
    page = 0
    while True:
        page_size = (curses.LINES -5) // 5
        if page_size > 10:
            page_size = 10

        stdscr.addstr(0, 0, "drokk\tpage " + str(page +1) + "/" + str(pages), curses.A_REVERSE)
        binds = 'r)eload | q)uit | 0..' + str(page_size -1) + ' select tweet | u)rl of selected tweet | n)ext page | p)rev page'
        stdscr.addstr(curses.LINES -1, 0, binds, curses.A_REVERSE)
 
        stdscr.refresh()
        c = stdscr.getkey()

        if c == 'q':
            break

        elif c == 'r':
            if selection > -1:
                reset_selection(selection, tweet_windows, stdscr)
            page = 0
            timeline = read_timeline()
            pages = math.ceil(len(timeline) / page_size)
            tweet_windows = load_tweets(timeline, page, page_size, win)
            
        elif c == 'u':
            curses.endwin()
            webbrowser.open(tweet["entities"]["urls"][0]["expanded_url"])
            curses.doupdate()

        elif c in ('n', 'l'):
            if page < pages -1:
                reset_selection(selection, tweet_windows, stdscr)
                selection = -1
                page += 1
                tweet_windows = load_tweets(timeline, page, page_size, win)

        elif c in ('p', 'h'):
            if page > 0:
                reset_selection(selection, tweet_windows, stdscr)
                selection = -1
                page -= 1
                tweet_windows = load_tweets(timeline, page, page_size, win)

        elif c == 'j':
            next_selection = 0
            if selection < len(tweet_windows) -1:
                next_selection = selection +1
            reset_selection(selection, tweet_windows, stdscr)
            selection = next_selection
            select_tweet(selection, tweet_windows, stdscr)

        elif c == 'k':
            next_selection = len(tweet_windows) -1
            if selection > 0:
                next_selection = selection -1
            reset_selection(selection, tweet_windows, stdscr)
            selection = next_selection
            select_tweet(selection, tweet_windows, stdscr)

        elif int(c) in list(range(0, page_size)):
            next_selection = int(c)
            reset_selection(selection, tweet_windows, stdscr)
            selection = next_selection
            if selection < len(tweet_windows):
                select_tweet(selection, tweet_windows, stdscr)
            else:
                selection = -1


def select_tweet(selection, tweet_windows, win):
    (y, x) = tweet_windows[selection].getbegyx()
    #tweet = timeline[selection + page * page_size]
    win.vline(y, x - 1, curses.ACS_VLINE, 3)
    #win.addstr(1,0,tweet["id_str"], curses.A_REVERSE)


def reset_selection(selection, tweet_windows, win):
    if selection > -1:
        (y, x) = tweet_windows[selection].getbegyx()
        win.vline(y, x - 1, ' ', 3)


def read_timeline():
    process = subprocess.Popen([
        'curl',
        '-s', 
        '-O', 
        'https://raw.githubusercontent.com/dgm9704/drokk/master/testoutput.json'],
        )
    process.wait()
    with open("testoutput.json", "r") as data:
        return json.load(data)

def load_tweets(timeline, page, page_size, win):
    win.erase()
    win.refresh()
    (y, x) = win.getyx()
    y += 3
    tweet_windows = {}
    t = 0
    first = page * page_size
    last = first + page_size 
    for tweet in timeline[first:last]:
        tw = curses.newwin(5, curses.COLS -3, y + t * 5 + 1, 3)
        output_tweet(tweet,tw)
        tweet_windows[t] = tw
        tw.refresh()
        t += 1
    return tweet_windows


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
    
    win.addstr("\n")

if __name__ == '__main__':
    wrapper(main)
