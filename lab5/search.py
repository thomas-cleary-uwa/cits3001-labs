""" show different search alogorithms """

import curses
import time
import random

from curses import wrapper

NUM_ROWS = 16
NUM_COLS = 16


def print_map(screen, search_map, queue=None):
    for row in search_map:
        for char in row:
            screen.addch(char)
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
                if search_map[at_y][at_x-1] == ".":
                    neighbours.append((at_x-1, at_y))

        if direction == 2: # up
            if not at_y - 1 < 0:
                if search_map[at_y-1][at_x] == ".":
                    neighbours.append((at_x, at_y-1)) 

        if direction == 3: # right
            if not at_x + 1 > len(search_map[0]) - 1:
                if search_map[at_y][at_x+1] == ".":
                    neighbours.append((at_x+1, at_y))

        if direction == 4: #down
            if not at_y + 1 > len(search_map) - 1:
                if search_map[at_y+1][at_x] == ".":
                    neighbours.append((at_x, at_y+1)) 

    return neighbours


def bfs(screen, search_map, at_x, at_y):
    queue = []

    queue.append((at_x, at_y))

    previous_node = None
    
    while len(queue) > 0:
        if previous_node is not None:
            search_map[previous_node[1]][previous_node[0]] = "o"

        current_node = queue.pop(0)
        cur_x, cur_y = current_node

        search_map[cur_y][cur_x] = "O"

        for neighbour in get_unvisited_neighbours(search_map, cur_x, cur_y):
            if neighbour not in queue:
                queue.append(neighbour)

        previous_node = current_node

        print_map(screen, search_map)
        screen.refresh()

        time.sleep(0.05)

        screen.clear()
    

def end(screen):
    time.sleep(3)
    screen.clear()
    screen.addstr("Goodbye\n")
    screen.refresh()
    time.sleep(1)


def main(args):
    screen = curses.initscr()

    search_map = [["."] * NUM_COLS for _ in range(NUM_ROWS)]

    at_x = 4
    at_y = 6
    search_map[at_y][at_x] = "O"

    # random_traverse(screen, search_map, at_x, at_y)
    bfs(screen, search_map, at_x, at_y)

    end(screen)


if __name__ == "__main__":
    wrapper(main)