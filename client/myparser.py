# python imports
from struct import pack, unpack

# project imports
from move import Move

class Parser:
    @staticmethod
    def decode(data):
        data = unpack('HB', data)
        if data[1] == 255:
            return data[0], None
        return data[0], Move(data[1] % 8, data[1] // 8)

    @staticmethod
    def encode(turn, move):
        if move == None:
            p = 255
        else:
            p = move.y * 8 + move.x
        return pack('HB', turn, p)
