""" Class to represent the board for Connect 4

Authors: Thomas Cleary
"""

import copy


class C4Board():

    def __init__(self):
        self.num_cols = 7
        self.num_rows = 6

        self.board     = None
        self.columns   = None
        self.rows      = None
        self.diagonals = None
        self.reset_board()

        self.pieces     = ["X", "O"]
        self.win_length = 4

        self.last_played = None
        self.winner      = None

    
    def get_new_board(self):
        """ return a board like the one given by the Lab6 tester """
        return (
            [[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)],
            ["" for _ in range(self.num_cols)],
            [" " for _ in range(self.num_rows)]
        )
        

    def reset_board(self):
        """ return the board to its original state """
        self.board, self.columns, self.rows = self.get_new_board()
        self.diagonals = self.get_diagonals() + self.get_diagonals(left_to_right=False)
    

    def get_diagonals(self, left_to_right=True):
        """ return the diagonal strings of the board """

        self.board = [[str(a) for a in range(7)] for _ in range(6)]

        diagonals = []

        # check first 3 cols where you start at left or rightmost column
        for start_row in range(2, -1, -1):
            diag = ""

            if left_to_right:
                col = 0
            else:
                col = self.num_cols - 1

            for row in range(start_row, self.num_rows):
                diag += self.board[row][col]

                if left_to_right:
                    col  += 1
                else:
                    col -= 1

            diagonals.append(diag)

        # check remaining 3 diagonals
        if left_to_right:
            col = 1
        else:
            col = self.num_cols - 2

        for _ in range(1, 4):
            diag = ""
            curr_col = col
            row = 0

            if left_to_right:
                while curr_col < self.num_cols:
                    diag += self.board[row][curr_col]
                    curr_col += 1
                    row += 1

            else:
                while curr_col >= 0:
                    print(row, curr_col)
                    diag += self.board[row][curr_col]
                    curr_col -= 1
                    row += 1

            diagonals.append(diag)
            if left_to_right:
                col += 1
            else:
                col -= 1

        return diagonals


    def add_piece(self, col_num, piece):
        """
        Add a piece to board at col_num if piece and column are valid
        Return True if piecce added, else False
        """
        if piece == self.last_played:
            raise ValueError("Same piece type played twice in a row")

        if self.is_col_full(col_num) or piece not in self.pieces:
            return False

        self.board[col_num]   += piece

        # add to column view
        self.columns[col_num] += piece

        # add to row view
        row_num = self.num_rows - len(self.columns[col_num])
        old_row = self.rows[row_num]
        self.rows[row_num] = old_row[:col_num] + piece + old_row[:self.num_cols]

        # update diagonals
        self.diagonals = self.get_diagonals() + self.get_diagonals(left_to_right=False)

        return True


    def is_col_full(self, col_num):
        """ return True if column is full else False """
        if col_num >= self.num_cols or col_num < 0:
            raise ValueError("Invalid column number")

        if len(self.board[col_num]) == self.num_rows:
            return True

        return False


    def is_full(self):
        """ return True if the board is full else False """
        for col in self.board:
            if len(col) < self.num_rows:
                return False
        return True


    def is_game_over(self):
        """ return True if game is over, else False """
        if self.is_full():
            self.winner = None
            return True

        x_win = self.pieces[0] * self.win_length
        o_win = self.pieces[1] * self.win_length

    
        is_over = self.is_over(self.columns) or \
                  self.is_over(self.rows)    or \
                  self.is_over(self.diagonals)


    def is_over(self, board):
        x_win = self.pieces[0] * self.win_length
        o_win = self.pieces[1] * self.win_length

        for line in board:
            if x_win in line:
                self.winner = "X"
                return True
            if o_win in line:
                self.winner = "O"
                return True

        return False

    