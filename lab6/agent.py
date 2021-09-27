""" CITS3001 Lab 6 - Thomas Cleary 21704985 """

import random

class C4Agent:

    def random_move(self, symbol, board, last_move):
        '''
        Make a random move unless center bottom is available
        '''

        # If we get to make the first move, go for the centre
        if last_move == -1 or len(board[3]) == 0:
            return 3

        while True:
            move = random.randint(0, 6)

            if len(board[move]) < 6:
                return move


    def move(self, symbol, board, last_move):
        '''
        symbol is the character that represents the agents moves in the board.
        symbol will be consistent throughout the game
        board is an array of 7 strings each describing a column of the board
        last_move is the column that the opponent last droped a piece into (or -1 if it is the firts move of the game).
        This method should return the column the agent would like to drop their token into.
        '''

        # If we get to make the first move, go for the centre
        if last_move == -1 or len(board[3]) == 0:
            return 3

        while True:
            move = random.randint(0, 6)

            if len(board[move]) < 6:
                return move


    
