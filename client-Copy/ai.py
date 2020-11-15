#python imports
from random import choice


def decide(wm):
    is_white = bool(wm.my_color)
    moves = wm.all_moves(is_white)
    if len(moves) == 0:
        return None
    return choice(moves)
