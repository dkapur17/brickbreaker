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