class Brick:
    def __init__(self,strength,length,x,y):
        self.strength = strength
        self.length = length
        self.x = x
        self.y = y
    def detect_collision(self, ball):
        self.strength -= 1

class Brick1(Brick):
    def __init__(self,length,x,y):
        super().__init__(1,length,x,y)
        self.content = ['1']*self.length

class Brick2(Brick):
    def __init__(self,length,x,y):
        super().__init__(2,length,x,y)
        self.content = ['2']*self.length
    
class Brick3(Brick):
    def __init__(self,length,x,y):
        super().__init__(3,length,x,y)
        self.content = ['3']*self.length

class BrickU(Brick):
    def __init__(self,length,x,y):
        super().__init__(-1,length,x,y)
        self.content = ['U']*self.length
    def detect_collision(self, ball):
        pass

class BrickE(Brick):
    def __init__(self,length,x,y):
        super().__init__(-2,length,x,y)
        self.content = ['E']*self.length
    def detect_collision(self,ball):
        pass