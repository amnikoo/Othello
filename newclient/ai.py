from worldmodel import WorldModel
from move import Move
def isOnCorner(move):
    return move.x in [0,7] and move.y in [0,7]
def copy(wm):
    WmCopy = WorldModel()
    for i in range (8):
        for j in range(8):
            WmCopy.board[i][j].is_empty = wm.board[i][j].is_empty
            WmCopy.board[i][j].is_white = wm.board[i][j].is_white
    WmCopy.white_team_name = wm.white_team_name
    WmCopy.black_team_name = wm.black_team_name
    WmCopy.my_color = wm.my_color
    return WmCopy
def MakeMove(wm,move,is_white):
    wm.board[move.x][move.y].is_empty = False
    wm.board[move.x][move.y].is_white = is_white
    neighbours = wm.neighbours ((move.x, move.y))
    partChanged=0
    for neighbour in neighbours.keys():
        if not neighbours[neighbour].is_empty and neighbours[neighbour].is_white != is_white:
            row = move.x+ neighbour[0]
            col = move.y+ neighbour[1]
            ally_found = False
            while (row >= 0 and row<=7) and (col>=0 and col<=7):
                if wm.board[row][col].is_empty:
                    break
                elif wm.board[row][col].is_white == is_white:
                    ally_found = True
                    break  
                row = row + neighbour[0]
                col = col + neighbour[1]
            if ally_found:
                row = move.x+ neighbour[0]
                col = move.y+ neighbour[1]
                while (row >= 0 and row<=7) and (col>=0 and col<=7):
                    if wm.board[row][col].is_white == is_white:
                        break  
                    wm.board[row][col].is_white = is_white
                    partChanged+=1
                    row = row + neighbour[0]
                    col = col + neighbour[1]
    return partChanged
def MoveRate(wm,move,is_white):
    wmCpy=copy(wm)
    score=MakeMove(wmCpy,move,is_white)
    Tree={move:{}}
    firstMoves = wmCpy.all_moves(not is_white)
    for first in firstMoves:
        wmCpy=copy(wm)
        score=MakeMove(wmCpy,move,is_white)
        score-=MakeMove(wmCpy,first,not is_white)
        Tree[move][first] = score
    TreeCpy=Tree.copy()
    firstSum=[]
    for first in Tree[move]:
        firstSum.append(TreeCpy[move][first])
    TreeCpy[move]= min(firstSum)
    return TreeCpy[move]
    
def decide(wm):
    is_white = bool(wm.my_color)
    possibleMoves = wm.all_moves(is_white)
    if len(possibleMoves)== 0:
        return None
    for move in possibleMoves:
        if isOnCorner(move):
            return move
    bestRate=-100
    for move in possibleMoves:
        Cpwm=copy(wm)
        MakeMove(Cpwm,move,is_white)
        if len(Cpwm.all_moves(not is_white))!=0:
            for nextmove in Cpwm.all_moves(not is_white):
                if isOnCorner(nextmove):
                    break
            if isOnCorner(nextmove):
                continue
        if MoveRate(wm,move,is_white)>bestRate:
            bestRate=MoveRate(wm,move,is_white)
            bestMove=move
    if bestRate==-100:
        for move in possibleMoves:
            if MoveRate(wm,move,is_white)>bestRate:
                bestRate=MoveRate(wm,move,is_white)
                bestMove=move
    return bestMove
