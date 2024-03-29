import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
import math

def isFree(x, y, board):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def is_game_over(board):
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
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
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            if board[i][j] == 0:
                legal_moves.append((i, j))
    return legal_moves

def make_move(board, x, y):
    if board[x][y] == 0:
        board[x][y] = 1
    else:
        pp.pipeOut("Error: illegal move")

def For_block_opp(board, player):
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
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
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
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
    
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
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

def check_up_right(board, i, j, player):
    if i - 4 >= 0 and j + 4 < pp.height:
        diagonal = [board[x][y] for x, y in zip(range(i, i - 5, -1), range(j, j + 5))]
        if diagonal == [player, player, player, 0, player]:
            return True, i - 3, j + 3
    return False, 0, 0

def check_up_left(board, i, j, player):
    if i - 4 >= 0 and j - 4 >= 0:
        diagonal = [board[x][y] for x, y in zip(range(i, i - 5, -1), range(j, j - 5, -1))]
        if diagonal == [player, player, player, 0, player]:
            return True, i - 3, j - 3
    return False, 0, 0

def checkVictory(board, player):
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            victory, x, y = check_up_right(board, i, j, player)
            victory2, z, w = check_up_left(board, i, j, player)
            if victory:
                print("YEEEAH THAT4S TRUE")
                return True, x, y
            elif victory2:
                print("YEEEAH THAT4S TRUE UP LEFT")
                return True, z, w
    return False, 0, 0

def placePionV2(board, i, j):
    if board[i][j] == 1 and board[i][j + 1] == 1 and board[i][j + 2] == 1 and board[i][j + 3] == 0 and board[i][j + 4] == 1:
        print("Found pattern horizontally")
        return True, i, j + 3
    elif board[i][j] == 1 and board[i + 1][j] == 1 and board[i + 2][j] == 1 and board[i + 3][j] == 0 and board[i + 4][j] == 1:
        print("Found pattern Vertically")
        return True, i + 3, j
    elif board[i][j] == 1 and board[i + 1][j + 1] == 1 and board[i + 2][j + 2] == 1 and board[i + 3][j + 3] == 0 and board[i + 4][j + 4] == 1:
        print("Found pattern Diagonally 1")
        return True, i + 3, j + 3
    elif board[i][j] == 1 and board[i - 1][j + 1] == 1 and board[i - 2][j + 2] == 1 and board[i - 3][j + 3] == 0 and board[i - 4][j + 4] == 1:
        print("Found pattern Diagonally 2")
        return True, i - 3, j + 3
    elif board[i][j] == 1 and board[i + 1][j - 1] == 1 and board[i + 2][j - 2] == 1 and board[i + 3][j - 3] == 0 and board[i + 4][j - 4] == 1:
        print("Found pattern Diagonally 3")
        return True, i + 3, j - 3
    elif board[i][j] == 1 and board[i - 1][j - 1] == 1 and board[i - 2][j - 2] == 1 and board[i - 3][j - 3] == 0 and board[i - 4][j - 4] == 1:
        print("Found pattern Diagonally 4")
        return True, i - 3, j - 3
    # other cases
    elif board[i][j] == 1 and board[i][j + 1] == 1 and board[i][j + 2] == 0 and board[i][j + 3] == 1 and board[i][j + 4] == 1:
        print("Found pattern horizontally")
        return True, i, j + 2
    elif board[i][j] == 1 and board[i + 1][j] == 1 and board[i + 2][j] == 0 and board[i + 3][j] == 1 and board[i + 4][j] == 1:
        print("Found pattern Vertically")
        return True, i + 2, j
    elif board[i][j] == 1 and board[i + 1][j + 1] == 1 and board[i + 2][j + 2] == 0 and board[i + 3][j + 3] == 1 and board[i + 4][j + 4] == 1:
        print("Found pattern Diagonally 1")
        return True, i + 2, j + 2
    elif board[i][j] == 1 and board[i - 1][j + 1] == 1 and board[i - 2][j + 2] == 0 and board[i - 3][j + 3] == 1 and board[i - 4][j + 4] == 1:
        print("Found pattern Diagonally 2")
        return True, i - 2, j + 2
    elif board[i][j] == 1 and board[i + 1][j - 1] == 1 and board[i + 2][j - 2] == 0 and board[i + 3][j - 3] == 1 and board[i + 4][j - 4] == 1:
        print("Found pattern Diagonally 3")
        return True, i + 2, j - 2
    elif board[i][j] == 1 and board[i - 1][j - 1] == 1 and board[i - 2][j - 2] == 0 and board[i - 3][j - 3] == 1 and board[i - 4][j - 4] == 1:
        print("Found pattern Diagonally 4")
        return True, i - 2, j - 2
    # other case
    elif board[i][j] == 1 and board[i][j + 1] == 0 and board[i][j + 2] == 1 and board[i][j + 3] == 1 and board[i][j + 4] == 1:
        print("Found pattern horizontally")
        return True, i, j + 1
    elif board[i][j] == 1 and board[i + 1][j] == 0 and board[i + 2][j] == 1 and board[i + 3][j] == 1 and board[i + 4][j] == 1:
        print("Found pattern Vertically")
        return True, i + 1, j
    elif board[i][j] == 1 and board[i + 1][j + 1] == 0 and board[i + 2][j + 2] == 1 and board[i + 3][j + 3] == 1 and board[i + 4][j + 4] == 1:
        print("Found pattern Diagonally 1")
        return True, i + 1, j + 1
    elif board[i][j] == 1 and board[i - 1][j + 1] == 0 and board[i - 2][j + 2] == 1 and board[i - 3][j + 3] == 1 and board[i - 4][j + 4] == 1:
        print("Found pattern Diagonally 2")
        return True, i - 1, j + 1
    elif board[i][j] == 1 and board[i + 1][j - 1] == 0 and board[i + 2][j - 2] == 1 and board[i + 3][j - 3] == 1 and board[i + 4][j - 4] == 1:
        print("Found pattern Diagonally 3")
        return True, i + 1, j - 1
    elif board[i][j] == 1 and board[i - 1][j - 1] == 0 and board[i - 2][j - 2] == 1 and board[i - 3][j - 3] == 1 and board[i - 4][j - 4] == 1:
        print("Found pattern Diagonally 4")
        return True, i - 1, j - 1
    else:
        victory, x, y = checkVictory(board, 1)
        if victory:
            return True, x, y
    return False, 0, 0

def hasToBlock(board, i, j):
    if board[i][j] == 2 and board[i][j + 1] == 2 and board[i][j + 2] == 2 and board[i][j + 3] == 0 and board[i][j + 4] == 2:
        print("Found pattern horizontally")
        return True, i, j + 3
    elif board[i][j] == 2 and board[i + 1][j] == 2 and board[i + 2][j] == 2 and board[i + 3][j] == 0 and board[i + 4][j] == 2:
        print("Found pattern Vertically")
        return True, i + 3, j
    elif board[i][j] == 2 and board[i + 1][j + 1] == 2 and board[i + 2][j + 2] == 2 and board[i + 3][j + 3] == 0 and board[i + 4][j + 4] == 2:
        print("Found pattern Diagonally 1")
        return True, i + 3, j + 3
    elif board[i][j] == 2 and board[i - 1][j + 1] == 2 and board[i - 2][j + 2] == 2 and board[i - 3][j + 3] ==   0 and board[i - 4][j + 4] == 2:
        print("Found pattern Diagonally 2")
        return True, i - 3, j + 3
    elif board[i][j] == 2 and board[i + 1][j - 1] == 2 and board[i + 2][j - 2] == 2 and board[i + 3][j - 3] == 0 and board[i + 4][j - 4] == 2:
        print("Found pattern Diagonally 3")
        return True, i + 3, j - 3
    elif board[i][j] == 2 and board[i - 1][j - 1] == 2 and board[i - 2][j - 2] == 2 and board[i - 3][j - 3] == 0 and board[i - 4][j - 4] == 2:
        print("Found pattern Diagonally 4")
        return True, i - 3, j - 3
    # other cases
    elif board[i][j] == 2 and board[i][j + 1] == 2 and board[i][j + 2] == 2 and board[i][j + 3] == 2 and board[i][j + 4] == 0:
        print("Found pattern horizontally")
        return True, i, j + 4
    elif board[i][j] == 2 and board[i + 1][j] == 2 and board[i + 2][j] == 2 and board[i + 3][j] == 2 and board[i + 4][j] == 0:
        print("Found pattern Vertically")
        return True, i + 4, j
    elif board[i][j] == 2 and board[i + 1][j + 1] == 2 and board[i + 2][j + 2] == 2 and board[i + 3][j + 3] == 2 and board[i + 4][j + 4] == 0:
        print("Found pattern Diagonally 1")
        return True, i + 4, j + 4
    elif board[i][j] == 2 and board[i - 1][j + 1] == 2 and board[i - 2][j + 2] == 2 and board[i - 3][j + 3] == 2 and board[i - 4][j + 4] == 0:
        print("Found pattern Diagonally 2")
        return True, i - 4, j + 4
    elif board[i][j] == 2 and board[i + 1][j - 1] == 2 and board[i + 2][j - 2] == 2 and board[i + 3][j - 3] == 2 and board[i + 4][j - 4] == 0:
        print("Found pattern Diagonally 3")
        return True, i + 4, j - 4
    elif board[i][j] == 2 and board[i - 1][j - 1] == 2 and board[i - 2][j - 2] == 2 and board[i - 3][j - 3] == 2 and board[i - 4][j - 4] == 0:
        print("Found pattern Diagonally 4")
        return True, i - 4, j - 4
    #Other case
    elif board[i][j] == 2 and board[i][j + 1] == 2 and board[i][j + 2] == 0 and board[i][j + 3] == 2 and board[i][j + 4] == 2:
        print("Found pattern horizontally")
        return True, i, j + 2
    elif board[i][j] == 2 and board[i + 1][j] == 2 and board[i + 2][j] == 0 and board[i + 3][j] == 2 and board[i + 4][j] == 2:
        print("Found pattern Vertically")
        return True, i + 2, j
    elif board[i][j] == 2 and board[i + 1][j + 1] == 2 and board[i + 2][j + 2] == 0 and board[i + 3][j + 3] == 2 and board[i + 4][j + 4] == 2:
        print("Found pattern Diagonally 1")
        return True, i + 2, j + 2
    elif board[i][j] == 2 and board[i - 1][j + 1] == 2 and board[i - 2][j + 2] == 0 and board[i - 3][j + 3] == 2 and board[i - 4][j + 4] == 2:
        print("Found pattern Diagonally 2")
        return True, i - 2, j + 2
    elif board[i][j] == 2 and board[i + 1][j - 1] == 2 and board[i + 2][j - 2] == 0 and board[i + 3][j - 3] == 2 and board[i + 4][j - 4] == 2:
        print("Found pattern Diagonally 3")
        return True, i + 2, j - 2
    elif board[i][j] == 2 and board[i - 1][j - 1] == 2 and board[i - 2][j - 2] == 0 and board[i - 3][j - 3] == 2 and board[i - 4][j - 4] == 2:
        print("Found pattern Diagonally 4")
        return True, i - 2, j - 2
    # other case
    elif board[i][j] == 2 and board[i][j + 1] == 0 and board[i][j + 2] == 2 and board[i][j + 3] == 2 and board[i][j + 4] == 2:
        print("Found pattern horizontally")
        return True, i, j + 1
    elif board[i][j] == 2 and board[i + 1][j] == 0 and board[i + 2][j] == 2 and board[i + 3][j] == 2 and board[i + 4][j] == 2:
        print("Found pattern Vertically")
        return True, i + 1, j
    elif board[i][j] == 2 and board[i + 1][j + 1] == 0 and board[i + 2][j + 2] == 2 and board[i + 3][j + 3] == 2 and board[i + 4][j + 4] == 2:
        print("Found pattern Diagonally 1")
        return True, i + 1, j + 1
    elif board[i][j] == 2 and board[i - 1][j + 1] == 0 and board[i - 2][j + 2] == 2 and board[i - 3][j + 3] == 2 and board[i - 4][j + 4] == 2:
        print("Found pattern Diagonally 2")
        return True, i - 1, j + 1
    elif board[i][j] == 2 and board[i + 1][j - 1] == 0 and board[i + 2][j - 2] == 2 and board[i + 3][j - 3] == 2 and board[i + 4][j - 4] == 2:
        print("Found pattern Diagonally 3")
        return True, i + 1, j - 1
    elif board[i][j] == 2 and board[i - 1][j - 1] == 0 and board[i - 2][j - 2] == 2 and board[i - 3][j - 3] == 2 and board[i - 4][j - 4] == 2:
        print("Found pattern Diagonally 4")
        return True, i - 1, j - 1
    else:
        victory, x, y = checkVictory(board, 2)
        if victory:
            return True, x, y
    return False, 0, 0

def placePion(board):
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            # Check the other cases than 1,1,1,0,1. Idem for the oppponent
            # test with diagonal
            place, x, z = placePionV2(board, i, j)
            if place:
                return x, z
            elif board[i][j] == 1:
                if (board[i + 1][j] == 1 or board[i - 1][j] == 1):
                    if (board[i + 1][j] == 0 and i + 1 <= pp.width):
                        print("1.1")
                        print(f"i = {i}, j = {j}")
                        return i + 1, j
                    elif (board[i - 1][j] == 0 and i - 1 >= 0):
                        print("1.2")
                        return i - 1, j
                elif (board[i][j + 1] == 1 or board[i][j - 1] == 1):
                    if (board[i][j + 1] == 0 and j + 1 <= pp.height):
                        print("2.1")
                        return i, j + 1
                    elif (board[i][j - 1] == 0 and j - 1 >= 0):
                        print("2.2")
                        return i, j - 1
                elif (board[i + 1][j + 1] == 1 or board[i - 1][j - 1] == 1 or board[i + 1][j - 1] == 1 or board[i - 1][j + 1] == 1):
                    if (board[i + 1][j + 1] == 0 and i + 1 <= pp.width and j + 1 <= pp.height):
                        board[i + 1][j + 1] = 1
                        victory, z, w = For_block_opp(board, 1)
                        if victory:
                            print("3.1")
                            board[i + 1][j + 1] = 0
                            print("YEH")
                            return z, w
                        continue
                    elif (board[i - 1][j - 1] == 0 and i - 1 >= 0 and j - 1 >= 0):
                        print("3.2")
                        return i - 1, j - 1
                    elif (board[i + 1][j - 1] == 0 and i + 1 <= pp.width and j - 1 >= 0):
                        print("3.3")
                        return i + 1, j - 1
                    elif (board[i - 1][j + 1] == 0 and i - 1 >= 0 and j + 1 <= pp.height):
                        print("3.4")
                        return i - 1, j + 1
                else:
                    if (board[i + 1][j] == 0 and i + 1 <= pp.width):
                        print("1")
                        print(f"i = {i}, j = {j}")
                        return i + 1, j
                    elif (board[i - 1][j] == 0 and i - 1 >= 0):
                        print("2")
                        return i - 1, j
                    elif (board[i][j + 1] == 0 and j + 1 <= pp.height):
                        print("3")
                        return i, j + 1
                    elif (board[i][j - 1] == 0 and j - 1 >= 0):
                        print("4")
                        return i, j - 1
                    elif (board[i + 1][j + 1] == 0 and i + 1 <= pp.width and j + 1 <= pp.height):
                        print("5")
                        return i + 1, j + 1
                    elif (board[i - 1][j - 1] == 0 and i - 1 >= 0 and j - 1 >= 0):
                        print("6")
                        return i - 1, j - 1
                    elif (board[i + 1][j - 1] == 0 and i + 1 <= pp.width and j - 1 >= 0):
                        print("7")
                        return i + 1, j - 1
                    elif (board[i - 1][j + 1] == 0 and i - 1 >= 0 and j + 1 <= pp.height):
                        print("8")
                        return i - 1, j + 1
    return 0, 0

def generate_patterns(board):
    patterns = []
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
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
