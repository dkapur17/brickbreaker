import json
import os
import random
from math import floor

from colorama import Fore

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

    def update(self,paddle,balls, bricks, on_screen_powerups, on_screen_bullets):
        self.clear()
        for brick in bricks:
            self.content[brick.y][brick.x: brick.x + brick.length] = brick.content
        for powerup in on_screen_powerups:
            self.content[floor(powerup.y)][powerup.x] = powerup.content
        for bullet in on_screen_bullets:
            self.content[bullet.y][bullet.x] = bullet.content
        for ball in balls:
            self.content[ball.y][ball.x] = ball.content
        self.content[paddle.y][paddle.x: paddle.x + paddle.curr_size] =  paddle.content