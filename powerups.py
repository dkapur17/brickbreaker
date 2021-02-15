from time import time

class PowerUp:
    def __init__(self,x,y,duration):
        self.x = x
        self.y = y
        self.inbound = True
        self.duration = duration
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
    def __init__(self,x,y,duration):
        super().__init__(x,y,duration)
        self.content = 'E'

    def activate(self,paddle,ball):
        super().activate()
        paddle.grow()
    
    def deactivate(self, paddle,ball):
        super().deactivate()
        paddle.reset_size()
