""" CITS3001 Lab3

Thomas Cleary 21704985
"""

from enum import Enum


class Cell(Enum):
    """ class for map cell states """
    UNKNOWN     = 0
    BLOCKED     = 1
    OPEN        = 2


def get_single_dict(cell_type):
    """ return a dict with cell type """
    return {"type": cell_type, "visited": False}

class MazeAgent():
    """ An agent to navigate a maze where the goal is at location (0, 0) """

    def __init__(self):
        self.goal = (0, 0)

        self.moves = []
        self.map   = [[get_single_dict(Cell.OPEN)]]
        self.location_order = []

        self.last_success_move = None


    def reset(self):
        """ reset the agent for a new maze """
        self.moves = []
        self.map   = [[get_single_dict(Cell.OPEN)]]
        self.location_order = []
        self.last_success_move = None


    def get_next_move(self, x, y):
        """ objective is to return a move L,R,U,D that will help reach (0, 0) """
        # check if agent moved
        if len(self.moves) > 1:
            if (x, y) != self.location_order[-1]:
                self.last_success_move = self.moves[-1]
        
        # add new location to order
        self.location_order.append((x, y))

        self.update_map(x, y)

        next_move = self.decide_move(x, y)

        # if we have already been to the next move before
        # block current cell as we are now back tracking
        next_location = self.get_next_location(next_move)

        if next_location in self.location_order:
            self.map[x][y] = get_single_dict(Cell.BLOCKED)

        self.moves.append(next_move)
        return next_move

    
    def get_next_location(self, move):
        """ return the location we will be attempting to move to """
        current_location = self.location_order[-1]

        next_x, next_y = current_location

        if   move == "L": next_x -= 1
        elif move == "R": next_x += 1
        elif move == "D": next_y -= 1
        else:             next_y += 1

        return (next_x, next_y)


    def decide_move(self, x, y):
        """ decide the next move the agent will make """
        # assuming no negative values
        # if x < y try and move left
        # if y < x try and move down
        if x <= y:
            if x > 0:
                if self.map[x-1][y]["type"] != Cell.BLOCKED:
                    return "L"
                elif self.map[x][y-1]["type"] != Cell.BLOCKED:
                    return "D"
            elif y > 0:
                if self.map[x][y-1]["type"] != Cell.BLOCKED:
                    return "D"
                
        elif y <= x:
            if y > 0:
                if self.map[x][y-1]["type"] != Cell.BLOCKED:
                    return "D"
                elif self.map[x-1][y]["type"] != Cell.BLOCKED:
                    return "L"
            elif x > 0:
                if self.map[x-1][y]["type"] != Cell.BLOCKED:
                    return "L"

        # If we can't move left or down, 
        # if last move was left, try not to go backwards so Up
        # if last move was down try not to go backwards so Right
        # else right then up
        if self.last_success_move == "D":
            if self.map[x+1][y]["type"] != Cell.BLOCKED:
                return "R"
        
        elif self.last_success_move == "L":
            if self.map[x][y+1]["type"] != Cell.BLOCKED:
                return "U"


        if self.map[x+1][y]["type"] != Cell.BLOCKED:
            return "R"

        if self.map[x][y+1]["type"] == Cell.BLOCKED:
            raise Exception("Agent is stuck")

        return "U"


    def update_map(self, x, y):
        """ update the map of the world with new information """
        self.extend_map(x, y)

        # note that we have visited this cell on the map
        self.map[x][y]["visited"] = True

        # if we have made at least 1 move so far
        if len(self.location_order) > 1:
            # if we are still at the same location
            if self.location_order[-2] == self.location_order[-1]:
                last_move = self.moves[-1]

                # mark the cell we attempted to move to as blocked
                if last_move == 'L':
                    self.map[x-1][y] = get_single_dict(Cell.BLOCKED)

                elif last_move == 'R':
                    self.map[x+1][y] = get_single_dict(Cell.BLOCKED)

                elif last_move == 'U':
                    self.map[x][y+1] = get_single_dict(Cell.BLOCKED)

                else: # last_move == 'D'
                    self.map[x][y-1] = get_single_dict(Cell.BLOCKED)


    def extend_map(self, x, y):
        """ this method is assuming positive only values of x and y """

        map_rows = len(self.map)
        map_cols = len(self.map[0])

        # add a rows to the map if we need to
        if map_rows < (x + 1): # first x row is 0 so length will be 1 but x=1 needs 2 rows
            for i in range((x+1) - map_rows):
                self.map.append([get_single_dict(Cell.OPEN)] * map_cols)
            # add final row of for unknown map depth
            self.map.append([get_single_dict(Cell.UNKNOWN)] * map_cols)
        
        # if we have moved into a previously unknown row
        if map_rows == (x + 1):
            # make row known
            for col_num, col in enumerate(self.map[-1][:-1]):
                self.map[-1][col_num] = get_single_dict(Cell.OPEN)

            # create new unknown row
            self.map.append([get_single_dict(Cell.UNKNOWN)] * map_cols)


        # add a columns to the map if we need to
        if map_cols < (y + 1):
            for row in self.map:
                for i in range((y+1) - map_cols):
                    row.append(get_single_dict(Cell.OPEN))
                # add unknown cell to boundary of map
                row.append(get_single_dict(Cell.UNKNOWN))

        # now make boundary round entirely unknown
        for cell_num in range(len(self.map[-1])):
            self.map[-1][cell_num] = get_single_dict(Cell.UNKNOWN)

        map_cols = len(self.map[0]) # get updated value

        # if we have moved into a previously unknown column
        if map_cols == (y + 1):
            # make column known
            for row_num in range(len(self.map[:x+1])):
                self.map[row_num][-1] = get_single_dict(Cell.OPEN)

            # create new unkown column
            for row_num in range(len(self.map)):
                self.map[row_num].append(get_single_dict(Cell.UNKNOWN))
                


    def print_map(self):
        """ show the current map 
        
        "." = open cell, "#" = blocked cell, "x" = current location,
        "?" = unknown cell, "G" = goal cell.
        """

        def print_cell(marker):
            """ print a cell marker """
            print("{: <4}".format(marker), end="")

        colnums = ["y" + str(y) for y in range(len(self.map[0]))]

        print_cell("")
        for num in colnums:
            print_cell(num)
        print("\n")

        for row_num, row in enumerate(self.map):
            print("{: <4}".format("x" + str(row_num)), sep="", end="")

            for col_num, cell in enumerate(row):
                if (row_num, col_num) == self.location_order[-1] and \
                   (row_num, col_num) == self.goal:
                     print_cell("W")

                elif (row_num, col_num) == self.location_order[-1]:
                    print_cell("x")

                elif (row_num, col_num) == self.goal:
                    print_cell("G")

                elif (row_num, col_num) == self.location_order[0]:
                    print_cell("S")

                elif (row_num, col_num) == self.location_order[-1]:
                    print_cell("x")

                elif cell["type"] == Cell.OPEN and cell["visited"]:
                    print_cell("~")

                elif cell["type"] == Cell.OPEN:
                    print_cell(".")

                elif cell["type"] == Cell.BLOCKED:
                    print_cell("#")

                else:
                    print_cell("?")
            print("\n")



def test_agent(maze):
    """ 3x3 maze """

    goal  = (0, 0)
    start_x, start_y = (len(maze) - 1, len(maze[0]) - 1)
    next_x, next_y = start_x, start_y

    agent = MazeAgent()
    agent.reset()

    num_moves = 0

    while next_x != 0 or next_y != 0:
        print("Move {}\nTelling agent current location ({}, {})\n".format(num_moves, next_x, next_y))
        move = agent.get_next_move(next_x, next_y)

        agent.print_map()
        print("Next Agent Move: {}\n(Last successful move: {})\n".format(move, agent.last_success_move))
        print("-" * 80 + "\n")

        if move == 'L':
            try:
                if maze[next_x-1][next_y] != Cell.BLOCKED:
                    next_x -= 1
            except:
                pass

        elif move == 'D':
            try:
                if maze[next_x][next_y-1] != Cell.BLOCKED:
                    next_y -= 1
            except:
                pass

        elif move == 'R':
            try:
                if maze[next_x+1][next_y] != Cell.BLOCKED:
                    next_x += 1
            except:
                pass

        else:
            try:
                if maze[next_x][next_y+1] != Cell.BLOCKED:
                    next_y += 1
            except:
                pass
        
        num_moves += 1

    
    print("Agent Reached the Goal")


def main():
    maze_3x3 = [
        [Cell.OPEN,    Cell.OPEN,    Cell.BLOCKED],
        [Cell.BLOCKED, Cell.OPEN,    Cell.OPEN],
        [Cell.BLOCKED, Cell.BLOCKED, Cell.OPEN],
    ]   


    """
    Maze Agent is Failing Density 40
    .....##...
    #.....#..#
    ..#.....##
    .###.##...
    ...##.....
    .#..#.....
    .....#..#.
    #.#..##...
    ..###..#..
    .##......#
    """

    """
    Failing Maze Density 50
    ####......
    ..##...###
    ##..#.##.#
    .##.#.##.#
    ###...####
    ##....##.#
    ##..#.#.#.
    .####..#.#
    ...#.#.#..
    .#.......#
    """

    maze_d50 = read_maze("./maze_d50.txt")
    test_agent(maze_d50)

def read_maze(filename):
    with open(filename, "r") as maze_file:
        upside_down_maze = []
        for index, line in enumerate(maze_file):
            line = line.strip()
            upside_down_maze.append([])
            for char in line:
                if char == ".":
                    new_cell = Cell.OPEN
                else:
                    new_cell = Cell.BLOCKED

                upside_down_maze[index].append(new_cell)

        return list(reversed(upside_down_maze))




if __name__ == "__main__":
    main()
