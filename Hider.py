import math
from Support import *
import random

class Hider:
    # Initialize a hider
    def __init__(self, map, N, M):
        self.posX = random.randin(0, M)
        self.posY = random.randint(0, N)
        while map[self.posY][self.posX] == 1:
            self.posX = random.randin(0, M)
            self.posY = random.randint(0, N)
        map[self.posY][self.posX] = 2

    # Funtion to get seeker's position if hider can observe him
    def observeSeeker(self, visions):
        for i in range(len(visions)):
            if self.map[visions[i][0]][visions[i][1]] == 3: return visions[i]
        return None
