from time import time
from utilities import fetch_configurations

DURATION = fetch_configurations('config.json')['powerup_duration']

class PowerUp:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.inbound = True
        self.duration = DURATION
        self.expired = False
    
    def move(self, HEIGHT):
        self.y += 0.5
        if self.y >= HEIGHT:
            self.inbound = False
    
    def activate(self):
        self.init_time = time()
        self.activated = True

    def check_completion(self):
        return time() - self.init_time >= self.duration

    def collected(self, paddle):
        return self.y == paddle.y and self.x in range(paddle.x, paddle.x + paddle.curr_size)
    
    def deactivate(self):
        self.expired = True


class ExpandPaddle(PowerUp):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.name = "expandPaddle"
        self.content = 'E'

    def activate(self,paddle,balls):
        super().activate()
        paddle.grow()
    
    def deactivate(self, paddle,balls):
        super().deactivate()
        paddle.reset_size()

class ShrinkPaddle(PowerUp):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.name = "shrinkPaddle"
        self.content = 'S'
    
    def activate(self,paddle,balls):
        super().activate()
        paddle.shrink()

    def deactivate(self,paddle,balls):
        super().deactivate()
        paddle.reset_size()

class FastBall(PowerUp):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.name = "fastBall"
        self.content = 'F'

    def activate(self,paddle,balls):
        super().activate()
        for ball in balls:
            ball.curr_multiplier = ball.max_multiplier
    
    def deactivate(self,paddle,balls):
        super().deactivate()
        for ball in balls:
            ball.curr_multiplier = 1

class PaddleGrab(PowerUp):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.name = "paddleGrab"
        self.content = 'G'
    
    def activate(self,paddle,balls):
        super().activate()
        for ball in balls:
            ball.sticky = True
    
    def deactivate(self,paddle,balls):
        super().deactivate()
        for ball in balls:
            ball.sticky = False

class MultiBall(PowerUp):
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.name = "multiBall"
        self.inbound = True
        self.content = 'M'
    
    def activate(self,paddle,balls):
        new_balls_list = []
        for ball in balls:
            new_balls_list.append(ball.make_twin())
        self.expired = True
        return balls+new_balls_list

class ThruBall(PowerUp):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.name = "thruBall"
        self.content = 'T'

    def activate(self,paddle,balls):
        super().activate()
        for ball in balls:
            ball.thru = True
    
    def deactivate(self, paddle, balls):
        super().deactivate()
        for ball in balls:
            ball.thru = False