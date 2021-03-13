import utilities

class Bullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.inbound = True
        self.vel_y  = -1
        self.content = '*'
    
    def move(self, board):
        self.y += self.vel_y
        brick_x = -1
        brick_y = -1
        if self.y <= 1:
            self.inbound = False
        elif board.content[self.y-1][self.x] in utilities.get_brick_chars():
            self.inbound = False
            brick_x = self.x
            brick_y = self.y - 1

        return brick_x,brick_y