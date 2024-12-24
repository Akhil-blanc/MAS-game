
import numpy as np
from typing import Optional, List, Tuple

class TicTacToe3D:
    def __init__(self):
        # 3x3x3 board
        self.board = np.zeros((3, 3, 3), dtype=int)
        self.player = 1  # 1 for player, 2 for AI
        
    def make_move(self, x: int, y: int, z: int, player: int) -> bool:
        """Make a move on the board"""
        if self.board[x][y][z] == 0:
            self.board[x][y][z] = player
            return True
        return False
        
    def check_win(self) -> Optional[int]:
        """Check for win conditions"""
        # Check each 2D plane
        for i in range(3):
            # Check horizontal planes
            if np.any(np.all(self.board[i] == 1, axis=1)): return 1
            if np.any(np.all(self.board[i] == 2, axis=1)): return 2
            # Check vertical planes
            if np.any(np.all(self.board[i] == 1, axis=0)): return 1
            if np.any(np.all(self.board[i] == 2, axis=0)): return 2
            
        # Check diagonals in each plane
        for i in range(3):
            if np.all(np.diag(self.board[i]) == 1) or \
               np.all(np.diag(np.fliplr(self.board[i])) == 1): return 1
            if np.all(np.diag(self.board[i]) == 2) or \
               np.all(np.diag(np.fliplr(self.board[i])) == 2): return 2
               
        # Check 3D diagonals
        diag1 = [self.board[i][i][i] for i in range(3)]
        diag2 = [self.board[i][i][2-i] for i in range(3)]
        diag3 = [self.board[i][2-i][i] for i in range(3)]
        diag4 = [self.board[i][2-i][2-i] for i in range(3)]
        
        for diag in [diag1, diag2, diag3, diag4]:
            if all(x == 1 for x in diag): return 1
            if all(x == 2 for x in diag): return 2
            
        return None

    def is_full(self) -> bool:
        """Check if board is full"""
        return np.all(self.board != 0)
        
    def get_valid_moves(self) -> List[Tuple[int, int, int]]:
        """Get all valid moves"""
        return [(x, y, z) for x in range(3) for y in range(3) 
                for z in range(3) if self.board[x][y][z] == 0]
                
    def print_board(self):
        """Print the current board state"""
        symbols = {0: ".", 1: "X", 2: "O"}
        print("\n3D Tic Tac Toe Board:")
        for z in range(3):
            print(f"\nLevel {z + 1}")
            for x in range(3):
                for y in range(3):
                    print(symbols[self.board[x][y][z]], end=" ")
                print()