##
## EPITECH PROJECT, 2023
## B-AIA-500-REN-5-1-gomoku-andrea.mancion
## File description:
## main
##

import sys
sys.path.append("./src")
import random
import platform
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import copy
from annexe_function import play_random_game, backpropagate, select_best_move, is_game_over, evaluate, For_block_opp, isFree, placePion, generate_patterns, find_best_move_for_pattern, hasToBlock

pp.infotext = 'name="AI", author="Andrea Mancion", version="1.0", country="France", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 50
board = [[0 for i in range(MAX_BOARD - 1)] for j in range(MAX_BOARD - 1)]

EASY = False
MEDIUM = True
HARD = False
PATTERN_MATCHING = False
ai_made_move = False
counter = 0

def isFreeSize():
    count = 0
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            if isFree(i, j, board):
                count += 1
    return count

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
        if isFree(x, y, board):
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
        if isFree(x, y, board):
            score = simulate(x, y)
            if score > best_score:
                best_move = (x, y)
                best_score = score
    if best_move is None:
        easy_mode(i)
    else:
        x, y = best_move
        pp.do_mymove(x, y)
        
def checkAiPion():
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            if board[i][j] == 1:
                return True
    return False

def pattern_matching_mode():
    num_simulations = 4
    best_move = None
    best_score = -1

    for _ in range(num_simulations):
        x = random.randint(0, pp.width - 1)
        y = random.randint(0, pp.height - 1)
        if pp.terminateAI:
            return
        if isFree(x, y):
            score = simulate(x, y)
            if score > best_score:
                best_move = (x, y)
                best_score = score

    all_patterns = generate_patterns(board)

    target_pattern = [0, 1, 1, 1, 0]
    for i, pattern in enumerate(all_patterns):
        if pattern == target_pattern:
            best_move = find_best_move_for_pattern(board, i, len(pattern))

    if best_move is not None:
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
            if checkAiPion():
                print("OK?")
                x, y = placePion(board)
                print(f"I {x} J {y}")
                pp.do_mymove(x, y)
            else:
                medium_mode(i)
        elif PATTERN_MATCHING:
            pattern_matching_mode()
    ai_made_move = False
    print("REEAL BOARD: ")
    for i in range(pp.width):
        row = [str(board[i][j]) for j in range(pp.height)]
        pp.pipeOut(" ".join(row))
    if is_game_over(board):
        pp.pipeOut("INFO game over")
        winner = evaluate(board)
        if winner == -1:
            pp.pipeOut("Winner is opponent")
        elif winner == 1:
            pp.pipeOut("Winner is AI")
        sys.exit(0)
    if isFreeSize() == 0:
        pp.pipeOut("INFO game over")
        pp.pipeOut("Draw")
        sys.exit(0)
        
def brain_my(x, y):
    if isFree(x,y, board):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))
        
def brain_end():
    pass

def brain_about():
    pp.pipeOut(pp.infotext)
    
def block_opponent_moves():
    global ai_made_move
    global counter
    if ai_made_move:
        return
    for i in range(pp.width - 1):
        for j in range(pp.height - 1):
            # WARNING didn't work when the player is about to win (Communication file)
            # Test with diagonal
            place, x, y = hasToBlock(board, i, j)
            if place:
                ai_made_move = True
                pp.do_mymove(x, y)
                return
            elif isFree(i, j, board):
                board[i][j] = 2
                victory, z, w = For_block_opp(board, 2)
                if victory:
                    if (isFree(z, w, board)):
                        board[i][j] = 0
                        ai_made_move = True
                        pp.do_mymove(z, w)
                    if counter == 0 or counter % 2 == 0:
                        counter += 1
                        print(f"JE VAIS LA JE BLOQUE {i} {j}")
                        board[i][j] = 0
                        print(f"AGAIN I {i} J {j}")
                        if (i == 0 and j == 0) or (i == 0 and j == pp.height - 1) or (i == pp.width - 1 and j == 0) or (i == pp.width - 1 and j == pp.height - 1):
                            print("case 1")
                            ai_made_move = True
                            pp.do_mymove(i, j)
                            return
                        elif i == 0 or j == 0 or i == pp.width - 1 or j == pp.height - 1:
                            print("case 2")
                            ai_made_move = True
                            pp.do_mymove(z, w)
                            return
                        else:
                            print("case 3")
                            ai_made_move = True
                            print(f"I {i} J {j}")
                            pp.do_mymove(i, j)
                            return
                    else:
                        counter += 1
                        print(f"JE VAIS LA JE BLOQUE {z} {w}")
                        print("BLOCK BOARD: ")
                        board[i][j] = 0
                        ai_made_move = True
                        print(f"I {z} J {w}")
                        pp.do_mymove(z, w)
                        return
                board[i][j] = 0
                
def brain_block_opponent(canBlock):
    print(canBlock)
    if canBlock:
        victory, z, w = For_block_opp(board, 1)
        if victory:
            print(f"I {z} J {w}")
            pp.do_mymove(z, w)
            if is_game_over(board):
                pp.pipeOut("INFO game over")
                winner = evaluate(board)
                if winner == -1:
                    pp.pipeOut("Winner is opponent")
                elif winner == 1:
                    pp.pipeOut("Winner is AI")
                sys.exit(0)
    if canBlock:
        block_opponent_moves()
    
def brain_opponents(x, y):
    if isFree(x, y, board):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))
        
def brain_block(x, y):
    if isFree(x, y, board):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))

pp.brain_init = brain_init
pp.brain_turn = brain_turn
pp.brain_my = brain_my
pp.brain_end = brain_end
pp.brain_about = brain_about
pp.brain_opponents = brain_opponents
pp.brain_block_opponent = brain_block_opponent
pp.brain_block = brain_block

def main():
    pp.main()

if __name__ == "__main__":
    main()