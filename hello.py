 
# hello.py

from curses import wrapper

def main(stdscr):
    stdscr.addstr("Hello World!!!")
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    wrapper(main)
