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

def is_not_wall(map, posY, posX):
    return map[posY][posX] != 1

# Function to check if a position in range of the 2D array
def pos_in_range(pos, N, M):
    return (pos[0] >= 0 and pos[0] < N and pos[1] >= 0 and pos[1] < M)

# Funtion to return list of distinct cells that an agent can observe
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
                if map[curPosY + i*direction[quarter][t][0]][curPosX + i*direction[quarter][t][1]] == 1:
                    res.pop()
                    nextPos1 = [curPosY + direction[quarter][t][0] + direction[quarter][3][0], curPosX + direction[quarter][t][1] + direction[quarter][3][1]]
                    nextPos2 = [curPosY + direction[quarter][t][0] + direction[quarter][4][0], curPosX + direction[quarter][t][1] + direction[quarter][4][1]]
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
            current_pos = [curPosY + direction[quarter][3+k][0], curPosX + direction[quarter][3+k][1]]
            if pos_in_range(current_pos, N, M) == False:
                break
            queue = []
            queue.append(current_pos)
            cnt = sum(range(rad))
            while len(queue) != 0 and cnt > 0:
                cnt -= 1
                current = queue.pop(0)
                nextPos1 = [current[0] + direction[quarter][0+k][0], current[1] + direction[quarter][0+k][1]]
                if pos_in_range(nextPos1, N, M): queue.append(nextPos1)

                nextPos2 = [current[0] + direction[quarter][1+k][0], current[1] + direction[quarter][1+k][1]]
                if pos_in_range(nextPos2, N, M): queue.append(nextPos2)

                if map[current[0]][current[1]] != 1:
                    res.append((current[0], current[1]))
                else:
                    if pos_in_range(nextPos1, N, M):
                        map[nextPos1[0]][nextPos1[1]] = 1
                    if pos_in_range(nextPos2, N, M):
                        map[nextPos2[0]][nextPos2[1]] = 1
                    
    res = list(set(res))
    res.pop(res.index((curPosY, curPosX)))
    return res
