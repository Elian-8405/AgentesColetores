import random

class simpleReactivAgent:
    def __init__(self, grid):
        self.grid = grid
        self.start = grid[random.randint(10)][random.randint(10)]
        self.pos = self.start
    
    def movimentation(self):
        for raw in self.grid:
            for col in self.grid:
                self.pos = self.grid[random.randint(0,10)][random.randint(0,10)]
                if(self.pos == 0):
                    