import numpy as np

class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1  # Default to player 1
        
    def set_first_player(self, player):
        # Set who moves first (1 for human, 2 for AI)
        self.current_player = player
    
    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[0][col] == 0
    
    def make_move(self, col):
        if not self.is_valid_move(col):
            return False
        
        # Find the lowest empty row in the selected column
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player  # Switch between 1 and 2
                return True
        return False
    
    def undo_move(self, col):
        for row in range(self.rows):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                self.current_player = 3 - self.current_player
                return True
        return False
    
    def check_winner(self):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row][col + 1] == 
                    self.board[row][col + 2] == self.board[row][col + 3]):
                    return self.board[row][col]
        
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row + 1][col] == 
                    self.board[row + 2][col] == self.board[row + 3][col]):
                    return self.board[row][col]
        
        # Check diagonal (+ve slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row - 1][col + 1] == 
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3]):
                    return self.board[row][col]
        
        # Check diagonal (-ve slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row + 1][col + 1] == 
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                    return self.board[row][col]
        
        # Check for draw
        if np.all(self.board != 0):
            return 0
        
        return None
    
    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.is_valid_move(col)]
    
    def is_terminal(self):
        return self.check_winner() is not None
    
    def get_state(self):
        return self.board.copy() 