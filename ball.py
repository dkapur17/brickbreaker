from random import choice
from math import ceil,floor

import utilities

class Ball():
    paddle_offset_ref = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
    def __init__(self, paddle):
        self.content = 'o'
        self.paddle_offset = choice(self.paddle_offset_ref)
        self.x = paddle.x + paddle.curr_size//2 + self.paddle_offset
        self.y = paddle.y -1
        self.vel_x = 0
        self.vel_y = 0
        self.on_paddle = True

    def launch(self):
        if not self.on_paddle:
            return
        self.on_paddle = False
        self.vel_y = -1
        self.vel_x = floor(self.paddle_offset/3) if self.paddle_offset > 0 else ceil(self.paddle_offset/3)
    
    def move(self, board, paddle):

        if self.on_paddle:
            return [True, -1, -1]

        self.x += self.vel_x
        self.x = max(1, self.x)
        self.x = min(self.x, board.width-2)

        self.y += self.vel_y
        self.y = max(1,self.y)
        self.y = min(self.y, board.height-1)

        if self.x in [1, board.width-2]:
            self.vel_x *= -1

        if self.y >= board.height-1:
            return [False, -1, -1]
        elif self.y <= 1:
            self.vel_y *= -1
        elif ((self.y + self.vel_y) == paddle.y) and ((self.x+self.vel_x) in range(paddle.x - 1, paddle.x + paddle.curr_size)):
            self.vel_y = -1
            self.paddle_offset = self.paddle_offset_ref[min(max(0,self.x - paddle.x),paddle.curr_size-1)]
            self.vel_x = floor(self.paddle_offset/3) if self.paddle_offset > 0 else ceil(self.paddle_offset/3)
        
        brick_x = -1
        brick_y = -1
        if  board.content[self.y + self.vel_y][self.x] in utilities.get_brick_chars():
            brick_y = self.y +self.vel_y
            brick_x = self.x
            self.vel_y *= -1
        elif board.content[self.y][max(0,min(self.x + (1 if self.vel_x > 0 else -1), board.width-1))] in utilities.get_brick_chars():
            brick_x = max(0,min(self.x + self.vel_x, board.width-1))
            brick_y = self.y
            self.vel_x *= -1
        elif board.content[self.y + self.vel_y][max(0,min(self.x + self.vel_x,board.width-1))] in utilities.get_brick_chars():
            brick_x = max(0, min(self.x + self.vel_x,board.width-1))
            brick_y = self.y + self.vel_y
            self.vel_x *= -1
            self.vel_y *= -1

        return [True, brick_x, brick_y]
        