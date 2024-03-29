from Support import *
import random
import copy
from readMaze import *

# Hider and seeker will use the same map.

def swap(map, pos1, pos2):
    map[pos1[0]][pos1[1]], map[pos2[0]][pos2[1]] = map[pos2[0]][pos2[1]], map[pos1[0]][pos1[1]]

class Hider:
    # Initialize a Hider
    def __init__(self, map, visible, pos):
        self.map = copy.deepcopy(map)
        self.current_pos = pos
        self.heuristic = visible
        
    def calculate_heuristic_manhattan(self, current, seeker):
        self.heuristic = abs(current[0] - seeker[0]) + abs(current[1] - seeker[1])
        
    def valid_moves(self, map, map_dimensions):
        moves = []
        if self.current_pos[0] > 0:
            if self.current_pos[1] > 0:
                if map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 0 or map[self.current_pos[0] - 1][self.current_pos[1] - 1] == 4:
                    moves.append("up-left")
            if self.current_pos[1] < map_dimensions[1] - 1:
                if map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 0 or map[self.current_pos[0] - 1][self.current_pos[1] + 1] == 4:
                    moves.append("up-right")
            if map[self.current_pos[0] - 1][self.current_pos[1]] == 0 or map[self.current_pos[0] - 1][self.current_pos[1]] == 4:
                moves.append("up")
        if self.current_pos[0] < map_dimensions[0] - 1:
            if self.current_pos[1] > 0:
                if map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 0 or map[self.current_pos[0] + 1][self.current_pos[1] - 1] == 4:
                    moves.append("down-left")
            if self.current_pos[1] < map_dimensions[1] - 1:
                if map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 0 or map[self.current_pos[0] + 1][self.current_pos[1] + 1] == 4:
                    moves.append("down-right")
            if map[self.current_pos[0] + 1][self.current_pos[1]] == 0 or map[self.current_pos[0] + 1][self.current_pos[1]] == 4:
                moves.append("down")
        if self.current_pos[1] > 0:
            if map[self.current_pos[0]][self.current_pos[1] - 1] == 0 or map[self.current_pos[0]][self.current_pos[1] - 1] == 4:
                moves.append("left")
        if self.current_pos[1] < map_dimensions[1] - 1:
            if map[self.current_pos[0]][self.current_pos[1] + 1] == 0 or map[self.current_pos[0]][self.current_pos[1] + 1] == 4:
                moves.append("right")
        return moves
    
    def seeker_in_vicinity(self, map, map_dimensions):
        vision = logic_vision(map, 2, self.current_pos[0], self.current_pos[1], map_dimensions[0], map_dimensions[1])
        for cell in vision:
            if map[cell[0]][cell[1]] == 3:
                return (True, cell)
        return (False, ())
    
    def generate(self, map, map_dimensions):
        successors = []
        for action in self.valid_moves(map, map_dimensions):
            pos = self.current_pos
            new_map = copy.deepcopy(map)
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
            successors.append(Hider(new_map, self.heuristic, pos))
        return successors
    
    def clone(self):
        return Hider(copy.deepcopy(self.map), self.heuristic, self.current_pos)
    
    def move(self, map: list[list[int]], map_dimensions: tuple[int, int], level = 3):
        if level < 3:
            return self.clone()
        else:
            is_in_vicinity, seeker_pos = self.seeker_in_vicinity(map, map_dimensions)
            if not is_in_vicinity:
                return self.clone()
            else:
                successors = self.generate(map, map_dimensions)
                best = None
                for successor in successors:
                    successor.calculate_heuristic_manhattan(successor.current_pos, seeker_pos)
                    if best == None or successor.heuristic > best.heuristic:
                        best = successor
                if best is not None:
                    swap(map, self.current_pos, best.current_pos)
                    return best
                else:
                    return self.clone()