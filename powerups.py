from time import time
from utilities import fetch_configurations

DURATION = fetch_configurations('config.json')['powerup_duration']

class PowerUp:
    def __init__(self,x,y,vel_x):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = -2
        self.inbound = True
        self.duration = DURATION
        self.expired = False
    
    def move(self, HEIGHT, WIDTH):
        
        self.vel_y += 0.5
        self.vel_y = min(self.vel_y, 1)

        self.x += self.vel_x
        self.y += self.vel_y

        self.x = max(1, self.x)
        self.x = min(self.x, WIDTH - 2)
        self.y = min(self.y, HEIGHT - 1)

        if self.x in [1, WIDTH - 2]:
            self.vel_x *=-1
        if self.y <= 1:
            self.vel_y *= -1

        if self.y >= HEIGHT-1:
            self.inbound = False
    
    def activate(self):
        self.init_time = time()
        self.activated = True

    def check_completion(self):
        return time() - self.init_time >= self.duration

    def collected(self, paddle):
        return int(self.y) == paddle.y and self.x in range(paddle.x, paddle.x + paddle.curr_size+1)
    
    def deactivate(self):
        self.expired = True

    def get_time_left(self):
        return f"{self.duration - (time() - self.init_time):.2f}s"


class ExpandPaddle(PowerUp):
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
        self.name = "expandPaddle"
        self.content = 'E'

    def activate(self,paddle,balls):
        super().activate()
        paddle.grow()
    
    def deactivate(self, paddle,balls):
        super().deactivate()
        paddle.reset_size()

class ShrinkPaddle(PowerUp):
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
        self.name = "shrinkPaddle"
        self.content = 'S'
    
    def activate(self,paddle,balls):
        super().activate()
        paddle.shrink()

    def deactivate(self,paddle,balls):
        super().deactivate()
        paddle.reset_size()

class FastBall(PowerUp):
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
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
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
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
    def __init__(self,x,y,vel_x):
        self.x,self.y = x,y
        self.vel_x, self.vel_y = vel_x, -1
        self.name = "multiBall"
        self.inbound = True
        self.content = 'M'
    
    def activate(self,paddle,balls):
        new_balls_list = []
        for ball in balls:
            new_balls_list.append(ball.make_twin())
        self.expired = True
        return balls+new_balls_list
    
    def get_time_left(self):
        pass

class ThruBall(PowerUp):
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
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

class LaserPaddle(PowerUp):
    def __init__(self,x,y,vel_x):
        super().__init__(x,y,vel_x)
        self.name = "laserPaddle"
        self.content = 'L'
    
    def activate(self, paddle, balls):
        super().activate()
        paddle.enableShooting()
    
    def deactivate(self, paddle, balls):
        super().deactivate()
        paddle.disableShooting()

def get_powerup_list(x,y,vel_x):
    return [ExpandPaddle(x,y,vel_x),ShrinkPaddle(x,y,vel_x), FastBall(x,y,vel_x), PaddleGrab(x,y,vel_x), MultiBall(x,y,vel_x), ThruBall(x,y,vel_x), LaserPaddle(x,y,vel_x)]