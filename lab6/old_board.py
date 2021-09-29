""" board for connect 4 game defined by question """

import copy
import re


class C4Board():

    def __init__(self):
        self.num_cols = 7
        self.num_rows = 6

        self.board = self.generate_board()

        self.pieces = ["X", "O"]

        self.winner = None


    def reset_board(self):
        self.board = self.generate_board()


    def generate_board(self):
        return ["" for _ in range(self.num_cols)]


    def is_full(self):
        for col in self.board:
            if len(col) < self.num_rows:
                return False

        return True


    def is_col_full(self, col_num):
        if len(self.board[col_num]) == self.num_rows:
            return True
        return False


    def add_piece(self, col_num, piece_type):
        if self.is_col_full(col_num):
            return False

        if piece_type not in self.pieces:
            return False

        self.board[col_num] = self.board[col_num] + piece_type
        return True


    def is_game_over(self):

        horizontal_board = self.get_horizontal_board()

        regex_col = "^[XO\s]*[{}]{{4}}[XO\s]*$"
        regex_row = "^[XO\s]*[{}]{{4}}[XO\s]*$"


        # check vertical 
        for column in self.board:

            if re.search(regex_col.format("X"), column):
                self.winner = "X"
                return True

            if re.search(regex_col.format("O"), column):
                return True
                self.winner = "O"

        
        # check horizontal
        for row in horizontal_board:

            if re.search(regex_row.format("X"), row):
                self.winner = "X"
                return True

            if re.search(regex_row.format("O"), row):
                return True
                self.winner = "O"


        # check diagonals
        diagonals = self.get_horizontal_strings(horizontal_board) + self.get_horizontal_strings(self.reverse_board(horizontal_board))

        regex = "^[X0\s]*[{}]{{4}}[X0\s]*$"

        for diag in diagonals:
            if re.search(regex.format("X"), diag):
                self.winner = "X"
                return True
            if re.search(regex.format("O"), diag):
                self.winner = "O"
                return True

        return False


    def get_full_board(self):
        full_board = copy.deepcopy(self.board)

        for col_num, col in enumerate(full_board):
            while len(full_board[col_num]) < self.num_rows:
                full_board[col_num] += " "

        return full_board
        
    
    def get_horizontal_board(self):
        full_board = self.get_full_board()
        return ["".join([col[-1 * i] for col in full_board]) for i in range(1, self.num_rows + 1)]


    
    def reverse_board(self, horizontal_board):
        flipped_board = []
        for row in horizontal_board:
            flipped_board.append("".join(list(reversed(row))))
        return flipped_board

    
    def get_horizontal_strings(self, horizontal_board):

        horizontals = []

        # left to right including main and above diags
        start_row = 0
        start_col = 0

        horizontals_added = 0

        curr_row = start_row
        curr_col = start_col

        while horizontals_added < 4:
            curr_row = start_row
            curr_col = start_col
            curr_top_string = ""
            curr_bottom_string = ""

            while curr_row < self.num_rows and curr_col < self.num_cols:
                curr_top_string += horizontal_board[curr_row][curr_col]

                # add to bottom diag if legal
                if curr_row != curr_col:
                    if curr_row < self.num_rows and curr_col < self.num_rows:
                        curr_bottom_string += horizontal_board[curr_col][curr_row]

                curr_row += 1
                curr_col += 1

            horizontals.append(curr_top_string)

            if len(curr_bottom_string) >= 4:
                horizontals.append(curr_bottom_string)

            start_col += 1
            horizontals_added += 1

        return horizontals



