 
# hello.py

import json
from curses import wrapper

def main(stdscr):

    with open("data.json","r") as data:
        timeline = json.load(data)

    for tweet in timeline:
        header = "@" + tweet["user"]["screen_name"] + " (" + tweet["user"]["name"] + ") :\n"
        content = "\t" + tweet["text"] + "\n"
        stdscr.addstr(header)
        stdscr.addstr(content)
        stdscr.addstr("\n")
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    wrapper(main)
