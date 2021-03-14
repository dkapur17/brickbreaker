class UFO:
    def __init__(self,x,y, lives):
        self.x = x
        self.y = y
        self.content = []
        self.content.append(list("    ___    "))
        self.content.append(list(" __/   \\__ "))
        self.content.append(list("/  '---'  \\"))
        self.content.append(list("'--_____--'"))
        self.width = 11
        self.height = 4
        self.lives = lives
        
    def move(self, x):
        self.x = x

    def test_collision(self, balls):
        ball = balls[0]
        collided = False
        if ball.vel_y < 0 and ball.y == self.y + self.height and ball.x in range(self.x, self.x + self.width):
            ball.vel_y *= -1
            self.lives -=1 
            collided = True
        elif ball.vel_y > 0 and ball.y == self.y and ball.x in range(self.x, self.x + self.width):
            ball.vel_y *= -1
            self.lives -=1 
            collided = True
        elif ball.vel_x > 0 and ball.y in range(self.y, self.y + self.height) and ball.x  == self.x:
            ball.vel_x *= -1
            self.lives -=1 
            collided = True
        elif ball.vel_x < 0 and ball.y in range(self.y, self.y + self.height) and ball.x == self.x + self.width:
            ball.vel_x *=-1
            self.lives -=1 
            collided = True
        elif ball.x in range(self.x, self.x + self.width) and ball.y in range(self.y, self.y + self.height):
            if ball.vel_y > 0:
                ball.y = self.y + self.height + 1
            elif ball.vel_y < 0:
                ball.y = self.y - 1
            ball.vel_y *= 1
            self.lives -=1 
            collided = True
        return collided
