from time import time

class PowerUp:
    def __init__(self):
        self.init_time = time()
    
    def check_completion(self):
        return time() - self.init_time >= 5