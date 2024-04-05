from copy import deepcopy 
import heapq
import math

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def push(self, item, priority, tiebreaker = 0):
        heapq.heappush(self.elements, (priority, tiebreaker, item))
    
    def pop(self):
        return heapq.heappop(self.elements)[2]

def is_not_wall(map, posY, posX):
    return map[posY][posX] != 1

# Function to check if a position in range of the 2D array
def pos_in_range(pos, N, M):
    return (pos[0] >= 0 and pos[0] < N and pos[1] >= 0 and pos[1] < M)

# Function to return list of distinct cells that an agent can observe
# curPosY: initial row of the agent
# curPosX: initial column of the agent
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
                if map[curPosY + i*direction[quarter][t][0]][curPosX + i*direction[quarter][t][1]] == 1 or map[curPosY + i*direction[quarter][t][0]][curPosX + i*direction[quarter][t][1]] == 7:
                    res.pop()
                    if i == 1:
                        nextPos1 = [curPosY + i*direction[quarter][t][0] + direction[quarter][3][0], curPosX + i*direction[quarter][t][1] + direction[quarter][3][1]]
                        nextPos2 = [curPosY + i*direction[quarter][t][0] + direction[quarter][4][0], curPosX + i*direction[quarter][t][1] + direction[quarter][4][1]]
                        # Danh dau o 10 neu bi chan o 1
                        if t == 0 and pos_in_range(nextPos1, N, M): 
                            map[nextPos1[0]][nextPos1[1]] = 1
                        # Danh dau o 14 neu bi chan o 3
                        elif t == 2 and pos_in_range(nextPos2, N, M): 
                            map[nextPos2[0]][nextPos2[1]] = 1
                        # Danh dau o 11 va 13 neu bi chan o 2
                        elif t == 1 and pos_in_range(nextPos1, N, M) and pos_in_range(nextPos2, N, M):        
                            map[nextPos1[0]][nextPos1[1]] = 1
                            map[nextPos2[0]][nextPos2[1]] = 1
                        # Dung ngay khi gap o bi chan
                    break

        for k in range(2):
            if curPosY + direction[quarter][3+k][0] >= 0 and curPosY + direction[quarter][3+k][0] <= N-1 and curPosX + direction[quarter][3+k][1] <= M-1 and curPosX + direction[quarter][3+k][1] >= 0: 
                if ((map[curPosY + direction[quarter][k][0]][curPosX + direction[quarter][k][1]] == 1 or map[curPosY + direction[quarter][k][0]][curPosX + direction[quarter][k][1]] == 7) and (map[curPosY + direction[quarter][k+1][0]][curPosX + direction[quarter][k+1][1]] == 1 or map[curPosY + direction[quarter][k+1][0]][curPosX + direction[quarter][k+1][1]] == 7)): 
                    map[curPosY + direction[quarter][3+k][0]][curPosX + direction[quarter][3+k][1]] = 1
                if map[curPosY + direction[quarter][3+k][0]][curPosX + direction[quarter][3+k][1]] != 1 and map[curPosY + direction[quarter][3+k][0]][curPosX + direction[quarter][3+k][1]] != 7:
                    res.append((curPosY + direction[quarter][3+k][0], curPosX + direction[quarter][3+k][1]))
                    if rad > 2:
                        # kiem tra o 10, 11 (hoac 13, 14) co nam trong bang va co bi chan boi cac o truoc khong
                        nextPosY1 = curPosY + direction[quarter][3+k][0] + direction[quarter][0+k][0]
                        nextPosX1 = curPosX + direction[quarter][3+k][1] + direction[quarter][0+k][1]
                        if nextPosY1 >= 0 and nextPosY1 < N and nextPosX1 >= 0 and nextPosX1 < M and map[nextPosY1][nextPosX1] != 1 and map[nextPosY1][nextPosX1] != 7:
                            res.append((nextPosY1, nextPosX1))
                        nextPosY2 = curPosY + direction[quarter][3+k][0] + direction[quarter][1+k][0]
                        nextPosX2 = curPosX + direction[quarter][3+k][1] + direction[quarter][1+k][1]
                        if nextPosY2 >= 0 and nextPosY2 < N and nextPosX2 >= 0 and nextPosX2 < M and map[nextPosY2][nextPosX2] != 1 and map[nextPosY2][nextPosX2] != 7:
                            res.append((nextPosY2, nextPosX2))
                
    res = list(set(res))
    res.pop(res.index((curPosY, curPosX)))
    return res
