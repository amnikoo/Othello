#python imports
from time import sleep
import copy

#project imports
from worldmodel import WorldModel
from connection import Connection
from gui import GUI
from myparser import Parser
import config
import ai


class Manager:
    def __init__(self):
        self.wm = WorldModel()
        self.conn = Connection()
        self.gui = GUI()


    def init(self):
        self.conn.connect(host=config.host, port=config.port)
        #name = input('Enter your name: ')
        name = config.name
        self.conn.send(name.encode('UTF-8'))

        my_color = self.conn.recv(1).decode()
        other_team_name = self.conn.recv(32).decode()

        if my_color == '1':
            white_team_name = name
            black_team_name = other_team_name
        elif my_color == '0':
            white_team_name = other_team_name
            black_team_name = name

        self.wm.init(white_team_name, black_team_name, int(my_color))

        self.gui.init(512, 512)


    def run(self):
        turn = 1
        while True:
            turn_color = turn % 2
            is_white = bool(turn_color)

            try:
                if self.wm.my_color == turn_color:
                    move = ai.decide(copy.deepcopy(self.wm))
                    self.conn.send(Parser.encode(turn, move))
            except:
                pass

            t, m = Parser.decode(self.conn.recv(3))
            if t == turn:
                self.wm.do_move(m, is_white)

            self.gui.show(self.wm)

            w, b = self.wm.result()
            if w + b == 64:
                if w > b:
                    print ('White wins!')
                elif w < b:
                    print ('Black wins!')
                else:
                    print ('Draw!')
                break

            turn += 1
            #print (self.wm)
            sleep(1)


        sleep(5)
        self.conn.disconnect()

