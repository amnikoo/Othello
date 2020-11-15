from part import Part
from move import Move


class WorldModel:
    def __init__(self):
        self.board = [[Part(is_empty=True) for _ in range(8)] for _ in range(8)]
        self.white_team_name = ''
        self.black_team_name = ''

    def __str__(self):
        res = ''
        for row in self.board:
            for part in row:
                if not part.is_empty:
                    res += ('+1' if part.is_white else '-1') + '\t'
                else:
                    res +=  '00\t'
            res += '\n'
        return res


    def init(self, white_name, black_name):
        self.board[3][3].is_empty = False
        self.board[3][3].is_white = True
        self.board[4][4].is_empty = False
        self.board[4][4].is_white = True

        self.board[3][4].is_empty = False
        self.board[3][4].is_white = False
        self.board[4][3].is_empty = False
        self.board[4][3].is_white = False

        self.white_team_name = white_name
        self.black_team_name = black_name


    def is_isolated (self, point):
        row = point[0]
        col = point[1]
        if row<7:
            if not self.board[row+1][col].is_empty:
                return False
            if col<7:
                if not self.board[row+1][col+1].is_empty:
                    return False
                if not self.board[row][col+1].is_empty:
                    return False
            if col>0:
                if not self.board[row+1][col-1].is_empty:
                    return False
                if not self.board[row][col-1].is_empty:
                    return False

        if row>0:
            if not self.board[row-1][col].is_empty:
                return False
            if col<7:
                if not self.board[row-1][col+1].is_empty:
                    return False
                if not self.board[row][col+1].is_empty:
                    return False
            if col>0:
                if not self.board[row-1][col-1].is_empty:
                    return False
                if not self.board[row][col-1].is_empty:
                    return False
        return True

    def neighbours (self, point):
        neighbours = {(-1, 0):Part(is_empty=True), (-1, -1):Part(is_empty=True), (-1, 1):Part(is_empty=True), (0, -1):Part(is_empty=True), (0, 1):Part(is_empty=True), (1, -1):Part(is_empty=True), (1, 1):Part(is_empty=True), (1, 0):Part(is_empty=True)}
        row = point[0]
        col = point[1]
        if row<7:
            if not self.board[row+1][col].is_empty:
                neighbours[(1, 0)] = Part(self.board[row+1][col].is_empty, self.board[row+1][col].is_white)
            if col<7:
                if not self.board[row+1][col+1].is_empty:
                    neighbours[(1, 1)] = Part(self.board[row+1][col+1].is_empty, self.board[row+1][col+1].is_white)
                if not self.board[row][col+1].is_empty:
                    neighbours[(0, 1)] = Part(self.board[row][col+1].is_empty, self.board[row][col+1].is_white)
            if col>0:
                if not self.board[row+1][col-1].is_empty:
                    neighbours[(1, -1)] = Part(self.board[row+1][col-1].is_empty, self.board[row+1][col-1].is_white)
                if not self.board[row][col-1].is_empty:
                    neighbours[(0, -1)] = Part(self.board[row][col-1].is_empty, self.board[row][col-1].is_white)

        if row>0:
            if not self.board[row-1][col].is_empty:
                neighbours[(-1, 0)] = Part(self.board[row-1][col].is_empty, self.board[row-1][col].is_white)
            if col<7:
                if not self.board[row-1][col+1].is_empty:
                    neighbours[(-1, 1)] = Part(self.board[row-1][col+1].is_empty, self.board[row-1][col+1].is_white)
                if not self.board[row][col+1].is_empty:
                    neighbours[(0, 1)] = Part(self.board[row][col+1].is_empty, self.board[row][col+1].is_white)
            if col>0:
                if not self.board[row-1][col-1].is_empty:
                    neighbours[(-1, -1)] = Part(self.board[row-1][col-1].is_empty, self.board[row-1][col-1].is_white)
                if not self.board[row][col-1].is_empty:
                    neighbours[(0, -1)] = Part(self.board[row][col-1].is_empty, self.board[row][col-1].is_white)
        return neighbours


    def all_empty_not_isolateds (self):
        not_isolateds = []
        for row in range(8):
            for col in range (8):
                if not self.is_isolated((row, col)) and self.board[row][col].is_empty:
                    not_isolateds.append ((row, col))
        return not_isolateds


    def all_moves(self,is_white):
        moves = []
        not_isolateds = self.all_empty_not_isolateds()
        for point in not_isolateds:
            part = self.board[point[0]][point[1]]
            neighbours = self.neighbours (point)
            for neighbour in neighbours.keys():
                if not neighbours[neighbour].is_empty and neighbours[neighbour].is_white != is_white:
                    row = point[0]+ neighbour[0]
                    col = point[1]+ neighbour[1]
                    ally_found = False
                    while (row >= 0 and row<=7) and (col>=0 and col<=7):
                        if self.board[row][col].is_empty:
                            break
                        elif self.board[row][col].is_white == is_white:
                            ally_found = True
                            break  
                        row = row + neighbour[0]
                        col = col + neighbour[1]
                    if ally_found:
                        moves.append (Move(point[0], point[1]))
        return moves

    def check_move(self,move, is_white):
        if not move:
            return False
        found = False
        for mov in self.all_moves (is_white):
            if mov.x == move.x and mov.y == move.y:
                found = True
                break
        return found

    def do_move (self, move, is_white):
        if not move:
            return
        self.board[move.x][move.y].is_empty = False
        self.board[move.x][move.y].is_white = is_white
        neighbours = self.neighbours ((move.x, move.y))
        for neighbour in neighbours.keys():
            if not neighbours[neighbour].is_empty and neighbours[neighbour].is_white != is_white:
                row = move.x+ neighbour[0]
                col = move.y+ neighbour[1]
                ally_found = False
                while (row >= 0 and row<=7) and (col>=0 and col<=7):
                    if self.board[row][col].is_empty:
                        break
                    elif self.board[row][col].is_white == is_white:
                        ally_found = True
                        break  
                    row = row + neighbour[0]
                    col = col + neighbour[1]
                if ally_found:
                    row = move.x+ neighbour[0]
                    col = move.y+ neighbour[1]
                    while (row >= 0 and row<=7) and (col>=0 and col<=7):
                        if self.board[row][col].is_white == is_white:
                            break  
                        self.board[row][col].is_white = is_white
                        row = row + neighbour[0]
                        col = col + neighbour[1]
    def result (self):
        wc=0
        bc=0
        for row in range(8):
            for col in range(8):
                if self.board[row][col].is_white == True:
                    wc = wc+1
                if self.board[row][col].is_white == False:
                    bc = bc+1
        return (wc, bc)

