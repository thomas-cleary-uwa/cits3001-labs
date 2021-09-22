""" show different search alogorithms """

import curses
import time
import random

from curses import wrapper

NUM_ROWS = 5
NUM_COLS = 10

UNDISCOVERED = "o"
DISCOVERED   = "."
IN_QUEUE     = "?"
CURR_POS     = "C"
EMPTY        = " "

NUM_RUNS = 10
ANIMATION_SPEED = 0.1



def print_map(screen, search_map, queue=None):
    for row in search_map:
        for char in row:
            if char == CURR_POS:
                screen.addch(CURR_POS, curses.color_pair(1))
            elif char == IN_QUEUE:
                screen.addch(IN_QUEUE, curses.color_pair(2))
            elif char == UNDISCOVERED:
                screen.addch(UNDISCOVERED, curses.color_pair(3))
            elif char == DISCOVERED:
                screen.addch(DISCOVERED, curses.color_pair(4))
            else:
                screen.addch(EMPTY)

        screen.addch("\n")
    screen.addch("\n")
    screen.addch("\n")

    if queue is not None:
        print(queue)


def random_move(search_map, at_x, at_y):
    search_map[at_y][at_x] = "."

    moved = False

    while not moved:
        next_move = random.randint(1, 4)

        if next_move == 1: # left
            if at_x - 1 < 0:
                continue
            at_x -= 1
            search_map[at_y][at_x] = "O"

        if next_move == 2: # up
            if at_y - 1 < 0:
                continue
            at_y -= 1
            search_map[at_y][at_x] = "O"

        if next_move == 3: # right
            if at_x + 1 > len(search_map[0]) - 1:
                continue
            at_x += 1
            search_map[at_y][at_x] = "O"

        if next_move == 4: #down
            if at_y + 1 > len(search_map) - 1:
                continue
            at_y += 1
            search_map[at_y][at_x] = "O"

        moved = True

    return (at_x, at_y)


def random_traverse(screen, search_map, at_x, at_y):

    search_map[at_y][at_x] = "O"

    print_map(screen, search_map)
    screen.refresh()
    time.sleep(0.5)
    screen.clear()

    while True:
        at_x, at_y = random_move(search_map, at_x, at_y)

        print_map(screen, search_map)
        screen.refresh()
        time.sleep(0.25)
        screen.clear()


def get_unvisited_neighbours(search_map, at_x, at_y):
    neighbours = []

    directions = list(range(1, 4+1))

    for direction in directions:
        if direction == 1: # left
            if not at_x - 1 < 0:
                if search_map[at_y][at_x-1] == UNDISCOVERED:
                    neighbours.append((at_x-1, at_y))

        if direction == 2: # up
            if not at_y - 1 < 0:
                if search_map[at_y-1][at_x] == UNDISCOVERED:
                    neighbours.append((at_x, at_y-1)) 

        if direction == 3: # right
            if not at_x + 1 > len(search_map[0]) - 1:
                if search_map[at_y][at_x+1] == UNDISCOVERED:
                    neighbours.append((at_x+1, at_y))

        if direction == 4: #down
            if not at_y + 1 > len(search_map) - 1:
                if search_map[at_y+1][at_x] == UNDISCOVERED:
                    neighbours.append((at_x, at_y+1)) 

    return neighbours


def bfs(screen, search_map, at_x, at_y):
    queue = []

    queue.append((at_x, at_y))

    previous_node = None
    
    while len(queue) > 0:
        if previous_node is not None:
            search_map[previous_node[1]][previous_node[0]] = DISCOVERED

        current_node = queue.pop(0)
        cur_x, cur_y = current_node

        search_map[cur_y][cur_x] = CURR_POS
        print_map(screen, search_map)
        screen.refresh()
        time.sleep(ANIMATION_SPEED)
        screen.clear()

        for neighbour in get_unvisited_neighbours(search_map, cur_x, cur_y):
            queue.append(neighbour)
            search_map[neighbour[1]][neighbour[0]] = IN_QUEUE
            previous_node = current_node

            print_map(screen, search_map)
            screen.refresh()
            time.sleep(ANIMATION_SPEED)
            screen.clear()

        previous_node = current_node
    

def end(screen):
    time.sleep(3)
    screen.clear()
    screen.addstr("Goodbye\n")
    screen.refresh()
    time.sleep(1)


def main(args):
    screen = curses.initscr()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

    for i in range(NUM_RUNS):
        screen.clear()

        search_map = [[UNDISCOVERED] * NUM_COLS for _ in range(NUM_ROWS)]

        at_x = random.randint(0, NUM_COLS-1)
        at_y = random.randint(0, NUM_ROWS-1)
        search_map[at_y][at_x] = "O"

        # random_traverse(screen, search_map, at_x, at_y)
        bfs(screen, search_map, at_x, at_y)

    end(screen)


if __name__ == "__main__":
    wrapper(main)