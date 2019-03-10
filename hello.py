 
# hello.py

import json
from curses import wrapper

def main(stdscr):
    stdscr.addstr("Hello World!!!")
    stdscr.refresh()
    stdscr.getch()
    with open("content.json","r") as data:
        content = json.load(data)

if __name__ == '__main__':
    wrapper(main)
