import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
import math

def isFree(x, y, board):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

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
        board[x][y] = 1
    else:
        pp.pipeOut("Error: illegal move")

def For_block_opp(board, player):
    for i in range(pp.width):
        for j in range(pp.height):
            if isFree(i, j, board) and (
                j + 4 < pp.height and all(board[i][j + k] == player for k in range(1, 5)) or
                j - 4 >= 0 and all(board[i][j - k] == player for k in range(1, 5)) or
                i + 4 < pp.width and all(board[i + k][j] == player for k in range(1, 5)) or
                i - 4 >= 0 and all(board[i - k][j] == player for k in range(1, 5)) or
                i + 4 < pp.width and j + 4 < pp.height and all(board[i + k][j + k] == player for k in range(1, 5)) or
                i - 4 >= 0 and j - 4 >= 0 and all(board[i - k][j - k] == player for k in range(1, 5)) or
                i - 4 >= 0 and j + 4 < pp.height and all(board[i - k][j + k] == player for k in range(1, 5)) or
                i + 4 < pp.width and j - 4 >= 0 and all(board[i + k][j - k] == player for k in range(1, 5))
            ):
                print(f"Victoire détectée pour le joueur {player} à la position {i}, {j}")
                return True, i, j
    return False, 0, 0
        
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
    
    if not isinstance(node, dict):
        node = {'total_score': 0, 'visit_count': 0, 'parent': None}
        board[x][y] = node
    
    node['total_score'] += result
    node['visit_count'] += 1
    
    while node['parent'] is not None:
        node = node['parent']
        if not isinstance(node, dict):
            node = {'total_score': 0, 'visit_count': 0, 'parent': None}
        node['total_score'] += result
        node['visit_count'] += 1

def select_best_move(board, x, y):
    moves = get_legal_moves(board)
    best_move = None
    best_score = float('-inf')
    
    for i in range(pp.width):
        for j in range(pp.height):
            node = board[i][j]
            if not isinstance(node, dict):
                node = {'total_score': 0, 'visit_count': 0, 'parent': None}
                board[i][j] = node
            if node['visit_count'] == 0:
                continue
            if x * y == 0:
                score = node['total_score'] / node['visit_count'] + 1.41 * (2 * 0 / node['visit_count']) ** 0.5
            else:
                score = node['total_score'] / node['visit_count']  + 1.41 * (2 * math.log(x * y) / node['visit_count']) ** 0.5
            if score > best_score:
                best_move = (i, j)
                best_score = score 
    return best_score

def check_up_right(board, i, j):
    if i - 4 >= 0 and j + 4 < pp.height:
        diagonal = [board[x][y] for x, y in zip(range(i, i - 5, -1), range(j, j + 5))]
        if diagonal == [1, 1, 1, 0, 1]:
            return True, i - 3, j + 3
    return False, 0, 0

def check_up_left(board, i, j):
    if i - 4 >= 0 and j - 4 >= 0:
        diagonal = [board[x][y] for x, y in zip(range(i, i - 5, -1), range(j, j - 5, -1))]
        if diagonal == [1, 1, 1, 0, 1]:
            return True, i - 3, j - 3
    return False, 0, 0

def checkVictory(board):
    for i in range(pp.width):
        for j in range(pp.height):
            victory, x, y = check_up_right(board, i, j)
            victory2, z, w = check_up_left(board, i, j)
            if victory:
                print("YEEEAH THAT4S TRUE")
                return True, x, y
            elif victory2:
                print("YEEEAH THAT4S TRUE UP LEFT")
                return True, z, w
    return False, 0, 0

def score_line(board, dir_i, dir_j, i, j):
    score = 0
    for x in range(5):
        new_i, new_j = i + (dir_i * x), j + (dir_j * x)
        if 0 <= new_i < pp.height and 0 <= new_j < pp.width:
            if board[new_i][new_j] == 1:
                score = score + 1

    return score

def evaluate_board(board,i, j):
    score = 0

    # HG, G, BG, B, BD, D, HD, H
    directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    for dir_i, dir_j in directions:
        score += score_line(board, dir_i, dir_j, i, j)

    return score

def findBestMove(boardScore):
    score = {"x": -1, "y": -1, "score": -1}

    for i in range(pp.width):
        for j in range(pp.height):
            if boardScore[i][j] > score.get("score"):
                score = {"x": i, "y": j, "score": boardScore[i][j]}
    return score.get("x"), score.get("y")

def placePion(board):
    boardScore = [[0 for i in range(pp.height)] for j in range(pp.width)]

    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] == 0:
                boardScore[i][j] = evaluate_board(board, i, j)
            if board[i][j] == 1:
                boardScore[i][j] = -1
            if board[i][j] == 2:
                boardScore[i][j] = -2

    print("--------------------------------------Score----------------------------")
    for x in range(pp.width):
        print(boardScore[x])
    print("--------------------------------------END Score----------------------------")

    print("findBestMove = " + findBestMove(boardScore).__str__())
    return findBestMove(boardScore)


def generate_patterns(board):
    patterns = []
    for i in range(pp.width):
        for j in range(pp.height):
            pattern = [board[i][j + k] for k in range(5) if j + k < pp.height]
            patterns.append(pattern)
    return patterns

def find_best_move_for_pattern(board, pattern_index, pattern_size):
    rows = pp.width - pattern_size + 1
    cols = pp.height if pattern_size == 1 else pp.height - pattern_size + 1
    x = pattern_index // cols
    y = pattern_index % cols

    for i in range(pattern_size):
        # Vérification horizontale
        if not isFree(x + i, y):
            return None

        # Vérification verticale
        if not isFree(x, y + i):
            return None

        # Vérification diagonale vers le bas
        if not isFree(x + i, y + i):
            return None

        # Vérification diagonale vers le haut
        if not isFree(x - i, y + i):
            return None
    return x, y
