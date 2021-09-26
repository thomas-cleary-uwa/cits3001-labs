""" board for connect 4 game defined by question """


class C4Board():

    def __init__(self):
        self.num_cols = 7
        self.num_rows = 6

        self.board = self.generate_board()

        self.pieces = ["X", "O"]


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
        """ NEED TO WRITE THIS!!! """
        return False
