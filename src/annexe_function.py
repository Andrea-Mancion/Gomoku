import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
import math

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
    if board[x][y] == 0:
        board[x][y] == 1
    else:
        pp.pipeOut("Error: illegal move")
        
def has_won(board, player):
    for i in range(pp.width):
        for j in range(pp.height):
            if (
                j + 4 < pp.height and all(board[i][j + k] == player for k in range(1, 5)) or
                i + 4 < pp.width and all(board[i + k][j] == player for k in range(1, 5)) or
                i + 4 < pp.width and j + 4 < pp.height and all(board[i + k][j + k] == player for k in range(1, 5)) or
                i - 4 >= 0 and j + 4 < pp.height and all(board[i - k][j + k] == player for k in range(1, 5))
            ):
                return True
    return False
    
def evaluate(board):
    if has_won(board, 1):
        return 1
    elif has_won(board, 2):
        return -1
    else:
        return 0

def play_random_game(board):
    while not is_game_over(board):
        legal_moves = get_legal_moves(board)
        if not legal_moves:
            break
        random_move = random.choice(legal_moves)
        make_move(board, random_move[0], random_move[1])
        
    return evaluate(board)

def backpropagate(board, x, y, result):
    node = board[x][y]
    
    node['total_score'] += result
    node['visit_count'] += 1
    
    while node['parent'] is not None:
        node = node['parent']
        node['total_score'] += result
        node['visit_count'] += 1

def select_best_move(board, x, y):
    moves = get_legal_moves(board)
    best_move = None
    best_score = float('-inf')
    
    for move in moves:
        node = board[move[0]][move[1]]
        if node['visit_count'] == 0:
            continue
        score = node['total_score'] / node['visit_count'] + 1.41 * (2 * math.log(x * y) / node['visit_count']) ** 0.5
        if score > best_score:
            best_move = move
            best_score = score
            
    return best_move