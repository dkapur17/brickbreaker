import json
import os
import random

class Board:
    def __init__(self, height, width):
        # Get board dimensions
        self.height = height
        self.width = width

        # Create an empty board
        self.clear()
    
    def clear(self):
        # Completely empty the board
        self.content = [[' ']*self.width for _ in range(self.height)]

        # Add Horizontal Boundaries
        self.content[0] = ['═']*self.width
        self.content[self.height-1] = ['═']*self.width

        # Add Vertical Boundaries
        for i in range(self.height): self.content[i][0] = '║'
        for i in range(self.height): self.content[i][self.width-1] = '║'

        # Add corners
        self.content[0][0]='╔'
        self.content[0][self.width-1]='╗'
        self.content[self.height-1][0]='╚'
        self.content[self.height-1][self.width-1]='╝'

    def update(self,paddle,ball):
        self.clear()
        self.content[paddle.y][paddle.x: paddle.x + paddle.curr_size] =  paddle.content
        self.content[ball.y][ball.x] = ball.content