#! /usr/bin/python

# python imports
from math import *
import pygame
from pygame.locals import *


class GUI:
    def __init__ (self):
        self.display_name = 'Othello AI'
        self.vertical_offset = 50
        self.font = None
        self.screen  = None


    def init(self, monitor_width, monitor_height):
        self.monitor_width  = monitor_width
        self.monitor_height = monitor_height
        self.piece_len = self.monitor_width // 8

        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height + 2 * self.vertical_offset))
        pygame.display.set_caption(self.display_name)



    def translate(self, row, col):
        x = col * self.piece_len
        y = row * self.piece_len + self.vertical_offset
        return x, y



    def reset_screen(self):
        self.screen.fill((0, 0, 0))
        for row in range(8):
            for col in range(8):
                color = (0, 160, 0)
                x, y = self.translate(row, col)
                pygame.draw.rect(self.screen, color, (x + 2, y + 2, self.piece_len - 4, self.piece_len - 4))


    def draw_piece(self, color, row, col):
        x, y = self.translate(row, col)
        x += self.piece_len // 2
        y += self.piece_len // 2
        pygame.draw.circle(self.screen, color, (x, y), self.piece_len // 2 - 5)


    def display_team_names(self, name, top):
        text_width, text_height = self.font.size(name)
        if top < 0:
            top += self.monitor_height + 2 * self.vertical_offset - text_height
        self.screen.blit(self.font.render(name, 1, (255, 255, 255)), ((self.screen.get_width() // 2) - text_width / 2, top))


    def show(self, wm):
        self.reset_screen()

        for row in range(len(wm.board)):
            for col in range(len(wm.board[row])):
                part = wm.board[row][col]
                if not part.is_empty:
                    color = (230, 230, 230) if part.is_white else (30, 30, 30)
                    self.draw_piece(color, row, col)

        self.display_team_names('black: ' + wm.black_team_name, 10)
        self.display_team_names('white: ' + wm.white_team_name, -10)

        #pygame.display.flip()
        pygame.display.update()

