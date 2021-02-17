from random import choice
from math import ceil,floor
import copy

import utilities

class Ball():
    def __init__(self, paddle, max_multiplier, curr_multiplier = 1, x=None, y=None, vel_x=0, vel_y=0, on_paddle=True, sticky=False, thru=False):
        self.content = 'o'
        self.paddle_offset_ref = list(range(-paddle.curr_size//2+1, paddle.curr_size//2 + 1))
        self.paddle_offset = choice(self.paddle_offset_ref)
        self.x = paddle.x + paddle.curr_size//2 + self.paddle_offset if x == None else x
        self.y = paddle.y -1 if y == None else y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.on_paddle = on_paddle
        self.inbound = True
        self.curr_multiplier = curr_multiplier
        self.max_multiplier = max_multiplier
        self.thru = thru
        self.sticky = sticky

    def make_twin(self):
        new_ball = copy.deepcopy(self)
        new_ball.vel_x *= -1
        return new_ball


    def launch(self):
        if not self.on_paddle:
            return
        self.on_paddle = False
        self.vel_y = -1
        self.vel_x = ceil(self.paddle_offset/3) if self.paddle_offset > 0 else floor(self.paddle_offset/3)
    
    def move(self, board, paddle):

        if self.on_paddle:
            return [True, -1, -1]

        self.x += floor(self.vel_x*self.curr_multiplier)
        self.x = max(1, self.x)
        self.x = min(self.x, board.width-2)

        self.y += self.vel_y
        self.y = max(1,self.y)
        self.y = min(self.y, board.height-1)

        self.paddle_offset_ref = list(range(-paddle.curr_size//2+1, paddle.curr_size//2 + 1))

        if self.x in [1, board.width-2]:
            self.vel_x *= -1

        if self.y >= board.height-1:
            return [False, -1, -1]
        elif self.y <= 1:
            self.vel_y *= -1
        elif ((self.y + self.vel_y) == paddle.y) and ((self.x+self.vel_x) in range(paddle.x - 1, paddle.x + paddle.curr_size)):
            if self.sticky:
                self.vel_x = 0
                self.vel_y = 0
                self.on_paddle = True
                self.paddle_offset = self.paddle_offset_ref[min(max(0,self.x - paddle.x),paddle.curr_size-1)]
            else:
                self.vel_y = -1
                self.paddle_offset = self.paddle_offset_ref[min(max(0,self.x - paddle.x),paddle.curr_size-1)]
                self.vel_x = ceil(self.paddle_offset/3) if self.paddle_offset > 0 else floor(self.paddle_offset/3)
        elif self.y == paddle.y and self.x in range(paddle.x, paddle.x+paddle.curr_size+1):
            self.y -= 1
            if self.sticky:
                self.vel_x = 0
                self.vel_y = 0
                self.on_paddle = True
                self.paddle_offset = self.paddle_offset_ref[min(max(0,self.x - paddle.x),paddle.curr_size-1)]
            else:
                self.vel_y = -1
                self.paddle_offset = self.paddle_offset_ref[min(max(0,self.x - paddle.x),paddle.curr_size-1)]
                self.vel_x = ceil(self.paddle_offset/3) if self.paddle_offset > 0 else floor(self.paddle_offset/3)
        
        brick_x = -1
        brick_y = -1
        if  board.content[self.y + self.vel_y][self.x] in utilities.get_brick_chars():
            brick_y = self.y +self.vel_y
            brick_x = self.x
            if not self.thru:
                self.vel_y *= -1
        elif board.content[self.y][max(0,min(self.x + (1 if self.vel_x > 0 else -1), board.width-1))] in utilities.get_brick_chars():
            brick_x = max(0,min(self.x + self.vel_x, board.width-1))
            brick_y = self.y
            if not self.thru:
                self.vel_x *= -1
        elif board.content[self.y + self.vel_y][max(0,min(self.x + self.vel_x,board.width-1))] in utilities.get_brick_chars():
            brick_x = max(0, min(self.x + self.vel_x,board.width-1))
            brick_y = self.y + self.vel_y
            if not self.thru:
                self.vel_x *= -1
                self.vel_y *= -1
        elif board.content[self.y][self.x] in utilities.get_brick_chars():
            brick_x = self.x
            brick_y = self.y
            self.y -= self.vel_y

        return [True, brick_x, brick_y]
        