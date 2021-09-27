""" Main script for testing the agent """

import random
import copy

from agent import C4Agent
from board import C4Board



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


WALL = bcolors.OKCYAN + "|" + bcolors.ENDC
ROOF = bcolors.OKCYAN + "-" + bcolors.ENDC


def get_printable_board(board):
    print_board = copy.deepcopy(board.board)

    for col_num, col in enumerate(print_board):
        while len(print_board[col_num]) < board.num_rows:
            print_board[col_num] += " "


    print_board = [[col[i * -1] for col in print_board] for i in range(1, board.num_rows + 1)]

    for str_index, string in enumerate(print_board):
        chars = list(string)

        for chr_index, char in enumerate(chars):
            if char == "X":
                colour = bcolors.FAIL
            elif char == "O":
                colour = bcolors.WARNING
            else:
                continue
            chars[chr_index] = colour + char + bcolors.ENDC

        print_board[str_index] = chars


    return print_board


def get_col_line(num_cols):

    col_line = []

    for i in range(0, num_cols):
        col_line.append(WALL)
        col_line.append(bcolors.OKBLUE + str(i) + bcolors.ENDC)
    col_line.append(WALL)

    return "".join(col_line)



def print_board(board):
    print_board = get_printable_board(board)

    col_line = get_col_line(board.num_cols)


    print()

    print("Agent = {}  Human = {}".format(
        bcolors.FAIL + "X" + bcolors.ENDC,
        bcolors.WARNING + "O" + bcolors.ENDC
    ))

    print()
    first_row = True
    for row in print_board:
        if first_row:
            first_row = False
        else:
            print(ROOF * 15)

        print(WALL, WALL.join(row), WALL, sep="")
    print(ROOF * 15)
    print(col_line)
    print()
    
    



def main():
    board = C4Board()

    agent = C4Agent()

    turn_order = random.randint(0, 1)
    if turn_order == 0:
        agent_turn  = True
    else:
        agent_turn = False

    agent_piece = board.pieces[0]
    human_piece = board.pieces[1]

    human_last_move = -1


    while not board.is_full() and not board.is_game_over():

        if agent_turn:
            agent_move = agent.move(
                agent_piece, board.board, human_last_move
            )
            valid_move = board.add_piece(agent_move, agent_piece)

            if not valid_move:
                print("Agent made an invalid move")
                break
            
            print("Agent played at {}".format(agent_move))
            print("-" * 20)
            agent_turn = False


        else:
            print_board(board)

            valid_move_made = False
            while not valid_move_made:
                try:
                    print("-" * 20)
                    move = int(input("Enter next move: "))
                except ValueError:
                    print("Enter a valid column number (0-6)")
                    continue

                if move < 0 or move > 6:
                    print("Enter a valid column number (0-6)")
                    continue

                valid_move = board.add_piece(move, human_piece)

                if valid_move:
                    print("-" * 20)
                    valid_move_made = True
                    agent_turn = True
                    human_last_move = move
                else:
                    print("Enter a valid column number (0-6)")


    print_board(board)

    if board.is_game_over():
        print("GAME OVER - ", end="")
        if board.winner == agent_piece:
            print(bcolors.FAIL + "Agent Won" + bcolors.ENDC)
        else:
            print(bcolors.WARNING + "Human Won" + bcolors.ENDC)

    else:
        print("Board is full")


if __name__ == "__main__":
    main()