import copy
from Support import PriorityQueue
import time  # for debugging purposes
from Support import logic_vision, Node
from readMaze import print_maze
from Hider import Hider
from Announcement import Announcement
import random

# 1 for wall
# 2 for hider
# 3 for seeker
# 0 for empty
# 4 for seeker's vision
# 5 for hider's vision
# 6 for announced cell

# Ô 1: 3 Ô 2: 6
# Ô 1 : 6 Ô 2 : 3

def swap(maze: list[list[int]], a: tuple[int, int], b: tuple[int, int]):
    if maze[a[0]][a[1]] == 3 and (maze[b[0]][b[1]] == 2 or maze[b[0]][b[1]] == 6):
        maze[b[0]][b[1]] = 3
        maze[a[0]][a[1]] = 0
    elif maze[b[0]][b[1]] == 3 and (maze[a[0]][a[1]] == 2 or maze[a[0]][a[1]] == 6):
        maze[a[0]][a[1]] = 3
        maze[b[0]][b[1]] = 0
    elif maze[a[0]][a[1]] == 2 and (maze[b[0]][b[1]] == 3 or maze[b[0]][b[1]] == 6):
        maze[b[0]][b[1]] = 3
        maze[a[0]][a[1]] = 0
    elif maze[b[0]][b[1]] == 2 and (maze[a[0]][a[1]] == 3 or maze[a[0]][a[1]] == 6):
        maze[a[0]][a[1]] = 3
        maze[b[0]][b[1]] = 0
    elif maze[a[0]][a[1]] == 6 and (maze[b[0]][b[1]] == 3 or maze[b[0]][b[1]] == 2):
        maze[b[0]][b[1]] = 3
        maze[a[0]][a[1]] = 0
    elif maze[b[0]][b[1]] == 6 and (maze[a[0]][a[1]] == 3 or maze[a[0]][a[1]] == 2):
        maze[a[0]][a[1]] = 3
        maze[b[0]][b[1]] = 0
    else:
        maze[a[0]][a[1]], maze[b[0]][b[1]] = maze[b[0]][b[1]], maze[a[0]][a[1]]
        
def calculate_heuristic_euclidean_wr(current: tuple[int, int], hider: tuple[int, int]) -> int:
    return ((current[0] - hider[0]) ** 2 + (current[1] - hider[1]) ** 2) ** 0.5


class Seeker:
    def __init__(self, map, visible, parent=None) -> None:
        self.map = self.format_map(copy.deepcopy(map))
        self.current_pos = self.current_pos_from_map(map)
        self.heuristic = visible
        self.action = ""
        self.parent = parent
        
    def calculate_heuristic_euclidean(self, current: tuple[int, int], hider: tuple[int, int]) -> int:
        self.heuristic = ((current[0] - hider[0]) ** 2 + (current[1] - hider[1]) ** 2) ** 0.5
        
    def format_map(self, map: list[list[int]]):
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 2:
                    map[i][j] = 0
        return map
        
    def calculate_heuristic_vision(self):
        heuristic = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 4:
                    heuristic += 1
        self.heuristic = heuristic
        
    def current_pos_from_map(self, map):
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 3:
                    return (i, j)
                
    def reset_known_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 4:
                    self.map[i][j] = 0
                    
    def reset_shared_map(self, map):
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 4:
                    map[i][j] = 0
        
    def get_current_pos(self):
        return self.current_pos
    
    def format_map_by_vision(self, vision: list[tuple[int, int]]):
        for cell in vision:
            if self.map[cell[0]][cell[1]] == 0:
                self.map[cell[0]][cell[1]] = 4
            
    def set_position(self, pos: tuple[int, int]):
        self.current_pos = pos
    
    def valid_moves(self, map: list[list[int]], map_dimensions: tuple[int, int], orthodox: bool = True) -> list[str]:
        moves = []
        if self.current_pos[0] > 0:
            if self.current_pos[1] > 0:
                if map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 0 or map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 4 or map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 2 or map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 6:
                    if orthodox:
                        moves.append("up-left")
            if self.current_pos[1] < map_dimensions[1] - 1:
                if map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 0 or map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 4 or map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 2 or map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 6:
                    if orthodox:
                        moves.append("up-right")
            if map[self.current_pos[0] - 1][self.current_pos[1]] == 0 or map[self.current_pos[0] - 1][self.current_pos[1]] == 4 or map[self.current_pos[0] - 1][self.current_pos[1]] == 2 or map[self.current_pos[0] - 1][self.current_pos[1]] == 6:
                moves.append("up")
        if self.current_pos[0] < map_dimensions[0] - 1:
            if self.current_pos[1] > 0:
                if map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 0 or map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 4 or map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 2 or map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 6:
                    if orthodox:
                        moves.append("down-left")
            if self.current_pos[1] < map_dimensions[1] - 1:
                if map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 0 or map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 4 or map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 2 or map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 6:
                    if orthodox:
                        moves.append("down-right")
            if map[self.current_pos[0] + 1][self.current_pos[1]] == 0 or map[self.current_pos[0] + 1][self.current_pos[1]] == 4 or map[self.current_pos[0] + 1][self.current_pos[1]] == 2 or map[self.current_pos[0] + 1][self.current_pos[1]] == 6:
                moves.append("down")
        if self.current_pos[1] < map_dimensions[1] - 1:
            if map[self.current_pos[0]][self.current_pos[1] + 1] == 0 or map[self.current_pos[0]][self.current_pos[1] + 1] == 4 or map[self.current_pos[0]][self.current_pos[1] + 1] == 2 or map[self.current_pos[0]][self.current_pos[1] + 1] == 6:
                moves.append("right")
        if self.current_pos[1] > 0:
            if map[self.current_pos[0]][self.current_pos[1] - 1] == 0 or map[self.current_pos[0]][self.current_pos[1] - 1] == 4 or map[self.current_pos[0]][self.current_pos[1] - 1] == 2 or map[self.current_pos[0]][self.current_pos[1] - 1] == 6:
                moves.append("left")
        return moves
    
    def generate(self, map: list[list[int]], map_dimensions: tuple[int, int], orthodox: bool = True):
        successors = []
        actions = self.valid_moves(map, map_dimensions, orthodox)
        for action in actions:
            pos = self.current_pos
            new_map = copy.deepcopy(self.map)
            if action == "up-right":
                swap(new_map, self.current_pos, (self.current_pos[0] - 1, self.current_pos[1] + 1))
                pos = (self.current_pos[0] - 1, self.current_pos[1] + 1)
            elif action == "up-left":
                swap(new_map, self.current_pos, (self.current_pos[0] - 1, self.current_pos[1] - 1))
                pos = (self.current_pos[0] - 1, self.current_pos[1] - 1)
            elif action == "up":
                swap(new_map, self.current_pos, (self.current_pos[0] - 1, self.current_pos[1]))
                pos = (self.current_pos[0] - 1, self.current_pos[1])
            elif action == "down-right":
                swap(new_map, self.current_pos, (self.current_pos[0] + 1, self.current_pos[1] + 1))
                pos = (self.current_pos[0] + 1, self.current_pos[1] + 1)
            elif action == "down-left":
                swap(new_map, self.current_pos, (self.current_pos[0] + 1, self.current_pos[1] - 1))
                pos = (self.current_pos[0] + 1, self.current_pos[1] - 1)
            elif action == "down":
                swap(new_map, self.current_pos, (self.current_pos[0] + 1, self.current_pos[1]))
                pos = (self.current_pos[0] + 1, self.current_pos[1])
            elif action == "left":
                swap(new_map, self.current_pos, (self.current_pos[0], self.current_pos[1] - 1))
                pos = (self.current_pos[0], self.current_pos[1] - 1)
            elif action == "right":
                swap(new_map, self.current_pos, (self.current_pos[0], self.current_pos[1] + 1))
                pos = (self.current_pos[0], self.current_pos[1] + 1)
            successors.append(Seeker(new_map, self.heuristic, self))
            successors[-1].set_position(pos)
            successors[-1].action = action
        return successors

    def __lt__(self, other):
        return self.heuristic < other.heuristic
            
    def move(self, maze: list[list[int]], map_dimensions: tuple[int, int]):
        frontier = PriorityQueue()
        successors = self.generate(maze, map_dimensions, False)
        for successor in successors:
            vision = logic_vision(maze, 3, successor.current_pos[0], successor.current_pos[1], map_dimensions[0], map_dimensions[1])
            successor.format_map_by_vision(vision)
            successor.calculate_heuristic_vision()
            if successor.heuristic > self.heuristic:
                frontier.push(successor, -successor.heuristic)
        if frontier.empty():
            return self.choose_random_unexplored_cell()
        next_move = frontier.pop()
        swap(maze, self.current_pos, next_move.current_pos)
        return next_move
    
    def move_to_pos(self, maze: list[list[int]], map_dimensions: tuple[int, int], pos: tuple[int, int]):
        successor = Seeker(copy.deepcopy(self.map), self.heuristic)
        swap(successor.map, successor.current_pos, pos)
        successor.set_position(pos)
        return successor
    
    def choose_random_unexplored_cell(self):
        pool = []
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 0:
                    pool.append((i, j))
        return random.choice(pool)
    
    def trace_hider(self, maze: list[list[int]], map_dimensions: tuple[int, int], hider_pos: Hider, visited: dict[tuple[tuple[int]]] = dict()):
        frontier = PriorityQueue()
        successors = self.generate(maze, map_dimensions)
        for successor in successors:
            successor.calculate_heuristic_euclidean(successor.current_pos, hider_pos)
            successor_tuple_map = tuple(map(tuple, successor.map))
            if successor_tuple_map not in visited or visited[tuple(map(successor.map))] < successor.heuristic:
                frontier.push(successor, successor.heuristic)
        next_move = frontier.pop()
        swap(maze, self.current_pos, next_move.current_pos)
        return next_move
    
    def clone(self):
        return Seeker(copy.deepcopy(self.map), self.heuristic)
    
    def reset_map_wr(self, map: list[list[int]]):
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 4:
                    map[i][j] = 0
        return map
    
    def furthest_from_self(self, cells: list[tuple[int, int]]) -> tuple[int, int]:
        furthest = (0, ())
        for cell in cells:
            distance = calculate_heuristic_euclidean_wr(self.current_pos, cell)
            if distance > furthest[0]:
                furthest = (distance, cell)
        if furthest[1] == ():
            print(cells)
        return furthest[1]
    
    def trace_random(self, maze: list[list[int]], map_dimensions: tuple[int, int], chosen_pos: tuple[int, int]):
        frontier = PriorityQueue()
        current = self.clone()
        current.calculate_heuristic_euclidean(current.current_pos, chosen_pos)
        frontier.push(current, current.heuristic)
        visited = dict()
        while not frontier.empty():
            current = frontier.pop()
            if current.current_pos == chosen_pos:
                return backtrace(current)
            successors = current.generate(maze, map_dimensions)
            for successor in successors:
                vision = logic_vision(maze, 3, successor.current_pos[0], successor.current_pos[1], map_dimensions[0], map_dimensions[1])
                successor.format_map_by_vision(vision)
                successor.calculate_heuristic_euclidean(successor.current_pos, chosen_pos)
                successor_tuple_map = tuple(map(tuple, self.reset_map_wr(successor.map)))
                if successor_tuple_map not in visited or visited[successor_tuple_map] < successor.heuristic:
                    visited[successor_tuple_map] = successor.heuristic
                    frontier.push(successor, successor.heuristic)
    
    def hider_in_vicinity(self, map: list[list[int]], map_dimensions: tuple[int, int]):
        vision = logic_vision(map, 3, self.current_pos[0], self.current_pos[1], map_dimensions[0], map_dimensions[1])
        nearest = (float("inf"), ())
        for cell in vision:
            if map[cell[0]][cell[1]] == 2:
                distance = calculate_heuristic_euclidean_wr(self.current_pos, cell)
                if distance < nearest[0]:
                    nearest = (distance, cell)
        if nearest[1] != ():
            return (True, nearest[1])
        return (False, ())

    def announce_in_vicinity(self, map: list[list[int]], map_dimensions: tuple[int, int]):
        vision = vision = logic_vision(map, 3, self.current_pos[0], self.current_pos[1], map_dimensions[0], map_dimensions[1])
        nearest = (float("inf"), ())
        for cell in vision:
            if map[cell[0]][cell[1]] == 6:
                distance = calculate_heuristic_euclidean_wr(self.current_pos, cell)
                if distance < nearest[0]:
                    nearest = (distance, cell)
        if nearest[1] != ():
            return (True, nearest[1])
        return (False, ())

    def caught_hider(self, list_hiders: list[Hider], map: list[list[int]], announcements: list[Announcement]):
        for i in range(len(list_hiders)):
            if self.current_pos == list_hiders[i].current_pos:
                if announcements[i]:
                    pos = announcements[i].get_pos()
                    for j in range(len(announcements)):
                        if j != i and announcements[j] and announcements[j].get_pos() == pos:
                            break
                        else:
                            continue
                    else:
                        if map[pos[0]][pos[1]] == 6:
                            map[pos[0]][pos[1]] = 0
                announcements.pop(i)
                list_hiders.pop(i)
                return True
        return False
    
def backtrace(node):
    path = []
    while node:
        path.append(node.current_pos)
        node = node.parent
    return path[::-1]