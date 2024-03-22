from copy import deepcopy 
import heapq
import math

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.elements)[1]
    
class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic = 0
        
    def calculate_heuristic(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] == 4:
                    self.heuristic += 1 #total number of observed cells
        return self.heuristic

# Funtion to return list of distinct cells that an agent can observe
# curPosY: initial row of the agent
# curPosX: initial column of the agent
def is_not_wall(map, posY, posX):
    return map[posY][posX] != 1

def logic_vision(realMap, rad, curPosY, curPosX, N, M):
    map = deepcopy(realMap)
    res = []
    res.append((curPosY, curPosX))
    # Directions to look in one quarter
    direction = [[(-1, 0), (-1, 1), (0, 1), (-2, 1), (-1, 2)],
                 [(0, 1), (1, 1), (1, 0), (1, 2), (2, 1)],
                 [(1, 0), (1, -1), (0, -1), (2, -1), (1, -2)],
                 [(0, -1), (-1, -1), (-1, 0), (-1, -2), (-2, -1)]]
    # Loop through 4 quarters of the vision's range
    for quarter in range(4):
        for t in range(3):
            for i in range(1, 1+rad):
                # Kiem tra co dang o hoac ke bien
                if curPosY + i*direction[quarter][t][0] < 0 or curPosX + i*direction[quarter][t][1] < 0 or curPosY + i*direction[quarter][t][0] >= N or curPosX + i*direction[quarter][t][1] >= M:
                    break        
                res.append((curPosY + i*direction[quarter][t][0], curPosX + i*direction[quarter][t][1]))     
                if map[curPosY + i*direction[quarter][t][0]][curPosX + i*direction[quarter][t][1]] == 1:
                    res.pop()
                    if i == 1 and rad == 3:
                        # Danh dau o 10 neu bi chan o 1
                        if t == 0: 
                            map[curPosY + direction[quarter][t][0] + direction[quarter][3][0]][curPosX + direction[quarter][t][1] + direction[quarter][3][1]] = 9
                        # Danh dau o 14 neu bi chan o 3
                        elif t == 2: 
                            map[curPosY + direction[quarter][t][0] + direction[quarter][4][0]][curPosX + direction[quarter][t][1] + direction[quarter][4][1]] = 9
                        # Danh dau o 11 va 13 neu bi chan o 2
                        else:                    
                            map[curPosY + direction[quarter][t][0] + direction[quarter][3][0]][curPosX + direction[quarter][t][1] + direction[quarter][3][1]] = 9
                            map[curPosY + direction[quarter][t][0] + direction[quarter][4][0]][curPosX + direction[quarter][t][1] + direction[quarter][4][1]] = 9
                    # Dung ngay khi gap o bi chan
                    break
        # Kiem tra neu o 5, o 7 bi chan
        if rad == 3:
            for k in range(2):
                if curPosY + direction[quarter][3+k][0] >= 0 and curPosY + direction[quarter][3+k][0] <= N-1 and curPosX + direction[quarter][3+k][1] <= M-1 and curPosX + direction[quarter][3+k][1] >= 0:
                    res.append((curPosY + direction[quarter][3+k][0], curPosX + direction[quarter][3+k][1]))
                    if map[curPosY + direction[quarter][3+k][0]][curPosX + direction[quarter][3+k][1]] != 1:
                        # Neu o 5 (hoac o 7) khong bi chan, kiem tra o 10, 11 (hoac 13, 14) co nam trong bang va co bi chan boi cac o truoc khong
                        nextPosY1 = curPosY + direction[quarter][3+k][0] + direction[quarter][0+k][0]
                        nextPosX1 = curPosX + direction[quarter][3+k][1] + direction[quarter][0+k][1]
                        if nextPosY1 >= 0 and nextPosY1 < N and nextPosX1 >= 0 and nextPosX1 < M and map[nextPosY1][nextPosX1] != 9:
                            res.append((nextPosY1, nextPosX1))
                        
                        nextPosY2 = curPosY + direction[quarter][3+k][0] + direction[quarter][1+k][0]
                        nextPosX2 = curPosX + direction[quarter][3+k][1] + direction[quarter][1+k][1]
                        if nextPosY2 >= 0 and nextPosY2 < N and nextPosX2 >= 0 and nextPosX2 < M and map[nextPosY2][nextPosX2] != 9:
                            res.append((nextPosY2, nextPosX2))
                    else:
                        res.pop()
    res = list(set(res))
    res.pop(res.index((curPosY, curPosX)))
    return res
