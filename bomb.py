class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 1
        self.content = '0'
        self.inbound = True
    
    def move(self, HEIGHT):
        self.y += self.vel_y
        if self.y >= HEIGHT - 1:
            self.inbound = False
    
    def detonate(self, paddle):
        if self.y == paddle.y and self.x in range(paddle.x, paddle.x + paddle.curr_size):
            paddle.lives -= 1
            self.inbound = False
            return True
        return False