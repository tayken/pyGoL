#!/usr/bin/python3

import curses
import getopt
import random
import sys
import time

# Conway's Game of Life universe
class universe:
    def __init__(self, width, height, tick):
        self.width = width
        self.height = height
        # Randomly generate seed status
        self.aliveNow  = [[bool(random.getrandbits(1)) for x in range(width)] for y in range(height)]
        self.aliveNext = [[None for x in range(width)] for y in range(height)]
        self.stdscr = curses.initscr()
        curses.halfdelay(tick)
        curses.curs_set(False)

    def calcNeighbors(self, x, y):
        return self.aliveNow[(y-1) % self.height][(x-1) % self.width] \
             + self.aliveNow[(y-1) % self.height][(x) % self.width]   \
             + self.aliveNow[(y-1) % self.height][(x+1) % self.width] \
             + self.aliveNow[(y) % self.height][(x-1) % self.width]   \
             + self.aliveNow[(y) % self.height][(x+1) % self.width]   \
             + self.aliveNow[(y+1) % self.height][(x-1) % self.width] \
             + self.aliveNow[(y+1) % self.height][(x) % self.width]   \
             + self.aliveNow[(y+1) % self.height][(x+1) % self.width]

    def nextRound(self):
        # Calculate results for next round
        for y in range(self.height):
            for x in range(self.width):
                neighborhood = self.calcNeighbors(x, y)
                self.aliveNext[y][x] = self.aliveNow[y][x]
                # If the cell is alive
                if self.aliveNow[y][x]:
                    # Death by underpopulation or overpopulation
                    if (neighborhood < 2) or (neighborhood > 3):
                        self.aliveNext[y][x] = False
                # If the cell is dead
                else:
                    # Life by reproduction
                    if neighborhood == 3:
                        self.aliveNext[y][x] = True

        # If our universe is not evolving, randomly start a new one
        if self.aliveNow == self.aliveNext:
            self.aliveNow  = [[bool(random.getrandbits(1)) for x in range(width)] for y in range(height)]
        # Otherwise swap now with next, clock ticked once
        else:
            self.aliveNow  = self.aliveNext
        self.aliveNext = [[None for x in range(self.width)] for y in range(self.height)]

    def dispCells(self):
        self.stdscr.clear()
        for y in range(self.height):
            for x in range(self.width):
                # Write a space char to position
                self.stdscr.addch(y, x, 32)
                # If it is alive, we can change it to a block
                if self.aliveNow[y][x]:
                    self.stdscr.addch(y, x, curses.ACS_BLOCK)
        self.stdscr.refresh()

    def cleanup(self):
        curses.curs_set(True)
        curses.endwin()

def main(argv):
    # Default arguments
    width  = 133
    height = 41
    tick = 2

    # Now try to parse them
    try:
        opts, args = getopt.getopt(argv, 'h:w:t:', ['height=','width=', 'tick='])
    except getopt.GetoptError:
        print('pyGoL.py -h <height> -w <width> -t <tick>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h' '--height'):
            height = int(arg)
        elif opt in ('-w', '--width'):
            width = int(arg)
        elif opt in ('-t', '--tick'):
            tick = int(arg)

    # Construct the universe and simulate until keypress is detected
    my = universe(width, height, tick)
    while True:
        char = my.stdscr.getch()
        my.dispCells()
        my.nextRound()
        if char != curses.ERR:
            break
    my.cleanup()

if __name__ == '__main__':
    main(sys.argv[1:])
