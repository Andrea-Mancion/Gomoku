##
## EPITECH PROJECT, 2023
## B-AIA-500-REN-5-1-gomoku-andrea.mancion
## File description:
## main
##

import random
import platform
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
from annexe_function import play_random_game, backpropagate, select_best_move, is_game_over, evaluate
import sys
sys.path.insert(1, "./src")

pp.infotext = 'name="AI", author="Andrea Mancion", version="1.0", country="France", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 50
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

EASY = False
MEDIUM = True
HARD = False
ai_made_move = False

def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR message - unsupported size or other error")
        return
    pp.pipeOut("OK - everything is good")
    
def simulate(x, y):
    simulate_board = copy.deepcopy(board)
    
    num_simulations = 4
    
    for _ in range(num_simulations):
        temp_board = copy.deepcopy(simulate_board)
        result = play_random_game(temp_board)
        backpropagate(simulate_board, x, y, result)
    node = simulate_board[x][y]
    if not isinstance(node, dict):
        node = {'total_score': 0, 'visit_count': 0, 'parent': None}
        simulate_board[x][y] = node
    best_score = select_best_move(simulate_board, x, y)
    
    return best_score
    
def easy_mode(i):
    while True:
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)
    
def medium_mode(i):
    num_simulations = 4
    best_move = None
    best_score = -1
    
    for _ in range(num_simulations):
        x = random.randint(0, pp.width)
        y = random.randint(0, pp.height)
        if pp.terminateAI:
            return
        if isFree(x, y):
            score = simulate(x, y)
            if score > best_score:
                best_move = (x, y)
                best_score = score
    if best_move is None:
        easy_mode(i)
    else:
        x, y = best_move
        pp.do_mymove(x, y)

    
def brain_turn():
    global ai_made_move
    if pp.terminateAI:
        return
    if ai_made_move == False:
        i = 0
        if EASY:
            easy_mode(i)
        elif MEDIUM:
            medium_mode(i)
    ai_made_move = False
    print("REEAL BOARD: ")
    for row in board:
        pp.pipeOut(" ".join(map(str, row)))
    if is_game_over(board):
        pp.pipeOut("INFO game over")
        winner = evaluate(board)
        if winner == -1:
            pp.pipeOut("Winner is opponent")
        elif winner == 1:
            pp.pipeOut("Winner is AI")
        sys.exit(0)
        
def brain_my(x, y):
    if isFree(x,y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))
        
def brain_end():
    pass

def brain_about():
    pp.pipeOut(pp.infotext)
    
def block_opponent_moves():
    global ai_made_move
    for i in range(pp.width):
        for j in range(pp.height):
            if isFree(i, j):
                board[i][j] = 2
                if evaluate(board) == -1:
                    print(f"JE VAIS LA JE BLOQUE {i} {j}")
                    board[i][j] = 0
                    ai_made_move = True
                    pp.do_mymove(i, j)
                    return
                board[i][j] = 0
    
def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
        block_opponent_moves()
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))
        
def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))

if DEBUG_EVAL and platform.system() == "Windows":
    import win32gui
    def brain_eval(x, y):
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2]-15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)
    

pp.brain_init = brain_init
pp.brain_turn = brain_turn
pp.brain_my = brain_my
pp.brain_end = brain_end
pp.brain_about = brain_about
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
if DEBUG_EVAL and platform.system() == "Windows":
    pp.brain_eval = brain_eval

def main():
    pp.main()

if __name__ == "__main__":
    main()