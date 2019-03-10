 
# hello.py

import json
from curses import wrapper

def main():# (stdscr):
    #stdscr.addstr("Hello World!!!")
    #stdscr.refresh()
    #stdscr.getch()

    with open("data.json","r") as data:
        content = json.load(data)

    for tweet in content:
        print("@" + tweet["user"]["screen_name"] + " (" + tweet["user"]["name"] + ") :")
        print("\t" + tweet["text"])
        #for k,v in tweet.items():
        #    print(k,v)
            #stdscr.addstr(str(v)) #str(k) + " -> " + str(v))
        print("\n")
        #stdscr.addstr("----------")
    
    #stdscr.refresh()
    #stdscr.getch()

if __name__ == '__main__':
    main()
    #wrapper(main)
