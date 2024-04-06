import random
import copy

class Announcement:
    def __init__(self, shared_map, N, M, hider_pos, hider):
        self.map = copy.deepcopy(shared_map)
        self.hider = hider
        while True:
            while True:
                x = hider_pos[0] + random.randint(-3,3)
                if x >= 0 and x < N: 
                    self.x = x
                    break
            while True:
                y = hider_pos[1] + random.randint(-3,3)
                if y >= 0 and y < M: 
                    self.y = y
                    break
            if shared_map[self.x][self.y] != 2 and shared_map[self.x][self.y] != 3 and shared_map[self.x][self.y] != 1 and shared_map[self.x][self.y] != 7:
                break
        self.map[self.x][self.y] = 6
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_info(self):
        prioritized = []
        for i in range(self.x - 3, self.x + 4):
            for j in range(self.y - 3, self.y + 4):
                if i >= 0 and i < len(self.map) and j >= 0 and j < len(self.map[0]):
                    if self.map[i][j] != 1 and self.map[i][j] != 7 and self.map[i][j] != 4 and self.map[i][j] != 6:
                        prioritized.append((i,j))
        return prioritized

