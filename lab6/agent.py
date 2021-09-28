""" CITS3001 Lab 6 - Thomas Cleary 21704985 """

import copy
import math
import random
import re

class C4Agent:

    def __init__(self):
        self.num_rows = 6
        self.num_cols = 7

        self.board    = ["" for _ in range(self.num_cols)]
        self.symbol   = None
        self.opponent_symbol = None

        self.chain_length_win = 4

    def move(self, symbol, board, last_move):
        '''
        symbol is the character that represents the agents moves in the board.
        symbol will be consistent throughout the game
        board is an array of 7 strings each describing a column of the board
        last_move is the column that the opponent last droped a piece into (or -1 if it is the firts move of the game).
        This method should return the column the agent would like to drop their token into.
        '''

        if self.symbol is None:
            self.symbol = symbol

            if self.symbol == "X":
                self.opponent_symbol = "O"
            else:
                self.opponent_symbol = "X"


        # If we get to make the first move, go for the centre
        if last_move == -1 or len(board[3]) == 0:
            return 3

        self.update_board(board)

        curr_board_value = self.evaluate_board(board)

        possible_moves = self.get_possible_moves()
        possible_boards = self.get_possible_boards(possible_moves, self.symbol)

        best_move = -1
        highest_value = -math.inf

        for move in possible_boards:
            value = self.evaluate_board(possible_boards[move])

            if value > highest_value:
                highest_value = value
                best_move = move

        if best_move > -1:
            return best_move

        while True:
            move = random.randint(0, self.num_cols - 1)

            if len(board[move]) < self.num_rows:
                return move



    def get_possible_moves(self):
        moves = []
        for move, column in enumerate(self.board):
            if len(column) < self.num_rows:
                moves.append(move)
        return moves


    def get_possible_boards(self, possible_moves, symbol):
        new_boards = {}

        for move in possible_moves:
            board_copy = copy.deepcopy(self.board)
            board_copy[move] += symbol
            new_boards[move] = board_copy

        return new_boards



    def evaluate_board(self, board):
        agent_chains    = [0] * self.chain_length_win
        opponent_chains = [0] * self.chain_length_win

        ### Check Column Chains ##############################################

        regex_piece_top = "^.*[{}]{{1}}$"

        for column in board:
            column_length = len(column)

            # only search column if it is not full or empty
            if column_length > 0 and column_length < self.num_rows:

                # if agent has a piece on top of the column
                if re.match(regex_piece_top.format(self.symbol), column) is not None:
                    # how long is the chain of agent pieces in this column?
                    self.add_column_chain(column, self.symbol, agent_chains)

                # if opponent piece on top
                elif re.match(regex_piece_top.format(self.opponent_symbol), column) is not None:
                    self.add_column_chain(column, self.opponent_symbol, opponent_chains)


        horizontal_board = self.get_horizontal_board(board)

        ### Check Row Chains ##################################################
        self.add_row_chains(horizontal_board, agent_chains, opponent_chains)

        ### Check Diagonal Chains #############################################
        self.add_diagonal_chains(horizontal_board, agent_chains, opponent_chains)

        return self.compute_board_value(agent_chains, opponent_chains)


    def add_column_chain(self, column, symbol, chains):
        column_empty_slots = self.num_rows - len(column)
        chain_length  = 0

        col_iter = reversed(column)

        try:
            while next(col_iter) == symbol:
                chain_length += 1

        except StopIteration:
            pass

        if chain_length + column_empty_slots >= self.chain_length_win:
            chains[chain_length - 1] += 1
    

    def add_row_chains(self, horizontal_board, agent_chains, opponent_chains):
        agent_set    = set([self.symbol, " "])
        opponent_set = set([self.opponent_symbol, " "])
        empty_sub_row_set = set([" "])

        ### Check rows for chains #############################################
        for row in horizontal_board:
            left = 0
            right = left + self.chain_length_win

            while right <= self.num_cols:
                sub_row = row[left:right]
                sub_row_set = set(sub_row)

                if sub_row_set <= agent_set and not sub_row_set == empty_sub_row_set:
                    symbol_count = sub_row.count(self.symbol)
                    if symbol_count > 0:
                        agent_chains[symbol_count-1] += 1

                elif sub_row_set <= opponent_set and not sub_row_set == empty_sub_row_set:
                    symbol_count = sub_row.count(self.opponent_symbol)
                    if symbol_count > 0:
                        opponent_chains[symbol_count-1] += 1

                left  += 1
                right += 1

    
    def add_diagonal_chains(self, horizontal_board, agent_chains, opponent_chains):
        agent_set    = set([self.symbol, " "])
        opponent_set = set([self.opponent_symbol, " "])
        empty_sub_diag_set = set([" "])

        diagonals = self.get_diagonal_strings(horizontal_board) + self.get_diagonal_strings(self.flip_board(horizontal_board))

        for diag in diagonals:
            diag_length = len(diag)
            left = 0
            right = left + self.chain_length_win

            while right <= diag_length:
                sub_diag = diag[left:right]
                sub_diag_set = set(sub_diag)

                if sub_diag_set <= agent_set and not sub_diag_set == empty_sub_diag_set:
                    symbol_count = sub_diag.count(self.symbol)

                    if symbol_count > 0:
                        agent_chains[symbol_count-1] += 1

                if sub_diag_set <= opponent_set and not sub_diag_set == empty_sub_diag_set:
                    symbol_count = sub_diag.count(self.opponent_symbol)
                    if symbol_count > 0:
                        opponent_chains[symbol_count-1] += 1

                left  += 1
                right += 1



    def compute_board_value(self, agent_chains, opponent_chains):
        if agent_chains[self.chain_length_win-1] > 0:
            return math.inf
        elif opponent_chains[self.chain_length_win-1] > 0:
            return -math.inf

        ONES_COEF   = 1
        TWOS_COEF   = 100
        THREES_COEF = 10000

        return (ONES_COEF   * agent_chains[1-1])    + \
               (TWOS_COEF   * agent_chains[2-1])    + \
               (THREES_COEF * agent_chains[3-1])    - \
               (ONES_COEF   * opponent_chains[1-1]) - \
               (TWOS_COEF   * opponent_chains[2-1]) - \
               (THREES_COEF * opponent_chains[3-1])



    def update_board(self, new_board):
        self.board = new_board


    def get_full_board(self, board):
        full_board = copy.deepcopy(board)

        for col_num, col in enumerate(full_board):
            while len(full_board[col_num]) < self.num_rows:
                full_board[col_num] += " "

        return full_board
        
    
    def get_horizontal_board(self, board):
        full_board = self.get_full_board(board)
        return ["".join([col[-1 * i] for col in full_board]) for i in range(1, self.num_rows + 1)]


    def flip_board(self, horizontal_board):
        flipped_board = []
        for row in horizontal_board:
            flipped_board.append("".join(list(reversed(row))))
        return flipped_board


    def get_diagonal_strings(self, horizontal_board):

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
            

    # def random_move(self, symbol, board, last_move):
    #     '''
    #     Make a random move unless center bottom is available
    #     '''

    #     # If we get to make the first move, go for the centre
    #     if last_move == -1 or len(board[3]) == 0:
    #         return 3

    #     while True:
    #         move = random.randint(0, 6)

    #         if len(board[move]) < 6:
    #             return move
    
