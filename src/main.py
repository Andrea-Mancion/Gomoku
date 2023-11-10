##
## EPITECH PROJECT, 2023
## B-AIA-500-REN-5-1-gomoku-andrea.mancion
## File description:
## main
##

import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="AI", author="Andrea Mancion", version="1.0", country="France", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 50
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

EASY = True
MEDIUM = False
HARD = False

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
    
def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    if EASY:
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

def brain_my(x, y):
    if isFree(x,y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))
        
def brain_end():
    pass

def brain_about():
    pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
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
if DEBUG_EVAL:
    pp.brain_eval = brain_eval

def main():
    pp.main()

if __name__ == "__main__":
    main()