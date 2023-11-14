import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy

def is_game_over(board):
    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] == 0:
                continue
            if j + 4 < pp.height and all(board[i][j + k] == board[i][j] for k in range(1, 5)):
                return True
            if i + 4 < pp.width and all(board[i + k][j] == board[i][j] for k in range(1, 5)):
                return True
            if i + 4 < pp.width and j + 4 < pp.height and all(board[i + k][j + k] == board[i][j] for k in range(1, 5)):
                return True
            if i - 4 >= 0 and j + 4 < pp.height and all(board[i - k][j + k] == board[i][j] for k in range(1, 5)):
                return True
    return False
    
def get_legal_moves(board):
    legal_moves = []
    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] == 0:
                legal_moves.append((i, j))
    return legal_moves

def make_move(board, x, y):
    print("TO DO")
    
def evaluate(board):
    print("TO DO")

def play_random_game(board):
    while not is_game_over(board):
        legal_moves = get_legal_moves(board)
        if not legal_moves:
            break
        random_move = random.choice(legal_moves)
        make_move(board, random_move[0], random_move[1])
        
    return evaluate(board)

def backpropagate(board, x, y, result):
    print("YEAH")

def select_best_move(board, x, y):
    print("YEAH")