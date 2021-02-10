class Paddle():

    def __init__(self, min_size, max_size, board_height, board_width, bottom_padding, speed, max_lives):
        self.min_size = min_size
        self.max_size = max_size
        self.curr_size = self.min_size
        self.content = ['▀']*self.curr_size
        self.board_width = board_width
        self.board_height = board_height
        self.bottom_padding = bottom_padding
        self.x = (self.board_width//2) - (self.curr_size//2)
        self.y = self.board_height - self.bottom_padding
        self.speed = speed
        self.lives = max_lives

    def move(self,direction, ball):
        if direction == 'left':
            movement = -1
        elif direction == 'right':
            movement = 1
        else:
            movement = 0
        self.x += movement*self.speed
        self.x = max(1, self.x)
        self.x = min(self.x, self.board_width - self.curr_size - 1)
        if ball.on_paddle:
            ball.x = self.x + self.curr_size//2 + ball.paddle_offset
    
    def reset(self):
        self.curr_size = self.min_size
        self.x = (self.board_width//2) - (self.curr_size//2)
        self.y = self.board_height - self.bottom_padding