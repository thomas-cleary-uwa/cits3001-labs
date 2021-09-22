""" show different search alogorithms """

import curses
import time
import random

from curses import wrapper

NUM_ROWS = 10
NUM_COLS = 10

UNDISCOVERED = "\U000025CB"
DISCOVERED   = "\U000025CF"
IN_QUEUE     = "\U000025CE"
CURR_POS     = "\U00002655"
WALL         = " "
GOAL         = "*"


NUM_RUNS = 1000
ANIMATION_SPEED = 0.15



def print_map(screen, search_map, goal_found=False, goal_in_queue=False):
    for row in search_map:
        for char in row:

            if char == CURR_POS:
                if not goal_found:
                    screen.addch(CURR_POS, curses.color_pair(1))
                else:
                    screen.addch(CURR_POS, curses.color_pair(7))

            elif char == IN_QUEUE:
                screen.addch(IN_QUEUE, curses.color_pair(2))

            elif char == UNDISCOVERED:
                screen.addch(UNDISCOVERED, curses.color_pair(3))

            elif char == DISCOVERED:
                screen.addch(DISCOVERED, curses.color_pair(4))

            elif char == WALL:
                screen.addch(WALL, curses.color_pair(5))

            elif char == GOAL:
                if goal_in_queue:
                    screen.addch(GOAL, curses.color_pair(8))
                else:
                    screen.addch(GOAL, curses.color_pair(6))


        screen.addch("\n")



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

    visitable = [UNDISCOVERED, GOAL]

    for direction in directions:
        if direction == 1: # left
            if not at_x - 1 < 0:
                if search_map[at_y][at_x-1] in visitable:
                    neighbours.append((at_x-1, at_y))

        if direction == 2: # up
            if not at_y - 1 < 0:
                if search_map[at_y-1][at_x] in visitable:
                    neighbours.append((at_x, at_y-1)) 

        if direction == 3: # right
            if not at_x + 1 > len(search_map[0]) - 1:
                if search_map[at_y][at_x+1] in visitable:
                    neighbours.append((at_x+1, at_y))

        if direction == 4: #down
            if not at_y + 1 > len(search_map) - 1:
                if search_map[at_y+1][at_x] in visitable:
                    neighbours.append((at_x, at_y+1)) 

    return neighbours


def bfs(screen, search_map, at_x, at_y):
    queue = []

    queue.append((at_x, at_y))

    previous_node = None

    goal_found = False
    goal_in_queue = False
    
    while len(queue) > 0 and not goal_found:
        if previous_node is not None:
            search_map[previous_node[1]][previous_node[0]] = DISCOVERED

        current_node = queue.pop(0)
        cur_x, cur_y = current_node

        if search_map[cur_y][cur_x] == GOAL:
            goal_found = True

        search_map[cur_y][cur_x] = CURR_POS
        print_map(screen, search_map, goal_found, goal_in_queue)
        screen.refresh()
        time.sleep(ANIMATION_SPEED)
        screen.clear()

        if goal_found:
            break



        for neighbour in get_unvisited_neighbours(search_map, cur_x, cur_y):
            queue.append(neighbour)
            if search_map[neighbour[1]][neighbour[0]] != GOAL:
                search_map[neighbour[1]][neighbour[0]] = IN_QUEUE
            else:
                goal_in_queue = True

            previous_node = current_node

            print_map(screen, search_map, goal_found, goal_in_queue)
            screen.refresh()
            time.sleep(ANIMATION_SPEED)
            screen.clear()

        previous_node = current_node



def add_walls(search_map, density=0.1):
    num_rows = len(search_map)
    num_cols = len(search_map[0])

    num_nodes = num_rows * num_cols

    num_walls = int(num_nodes * density)

    walls_added = 0

    while walls_added < num_walls:
        rand_row = random.randint(0, num_rows-1)
        rand_col = random.randint(0, num_cols-1)

        if search_map[rand_row][rand_col] == UNDISCOVERED:
            search_map[rand_row][rand_col] = WALL
            walls_added += 1


def add_goal(search_map):
    num_rows = len(search_map)
    num_cols = len(search_map[0])

    goal_added = False

    while not goal_added:
        rand_row = random.randint(0, num_rows-1)
        rand_col = random.randint(0, num_cols-1)

        if search_map[rand_row][rand_col] != CURR_POS:
            search_map[rand_row][rand_col] = GOAL
            goal_added = True




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
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)

    for i in range(NUM_RUNS):
        screen.clear()


        search_map = [[UNDISCOVERED] * NUM_COLS for _ in range(NUM_ROWS)]

        at_x = random.randint(0, NUM_COLS-1)
        at_y = random.randint(0, NUM_ROWS-1)
        # at_x = len(search_map[0]) - 1
        # at_y = 0
        search_map[at_y][at_x] = CURR_POS

        add_walls(search_map, density=0.3)
        add_goal(search_map)

        # random_traverse(screen, search_map, at_x, at_y)
        bfs(screen, search_map, at_x, at_y)
        time.sleep(2)

    end(screen)


if __name__ == "__main__":
    wrapper(main)