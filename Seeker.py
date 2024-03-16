from Support import *
import copy

# 1 for wall
# 2 for hider
# 3 for seeker
# 0 for empty
# 4 for seeker's vision
# 5 for hider's vision
# 6 for announced cell
# 7 for vision blocked cell

def swap(map: list[list[int]], pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    map[pos1[0]][pos1[1]], map[pos2[0]][pos2[1]] = map[pos2[0]][pos2[1]], map[pos1[0]][pos1[1]]

def get_map_center(map: list[list[int]]) -> tuple[int, int]:
    return (len(map) // 2, len(map[0]) // 2)

def get_current_pos(map: list[list[int]], agent: int) -> tuple[int, int]:
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == agent:
                return (i, j)
            
def get_value_pos(map: list[list[int]], value: int) -> tuple[int, int]:
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == value:
                return (i, j)

class Seeker:
    def __init__(self):
        self.start_pos = (0, 0)
        self.cur_pos = self.start_pos
        self.vision_range = 3
        
    def move(self, action):
        if action == "up":
            swap(map, self.cur_pos, (self.cur_pos[0] - 1, self.cur_pos[1]))
        elif action == "down":
            swap(map, self.cur_pos, (self.cur_pos[0] + 1, self.cur_pos[1]))
        elif action == "left":
            swap(map, self.cur_pos, (self.cur_pos[0], self.cur_pos[1] - 1))
        elif action == "right":
            swap(map, self.cur_pos, (self.cur_pos[0], self.cur_pos[1] + 1))
        elif action == "up-left":
            swap(map, self.cur_pos, (self.cur_pos[0] - 1, self.cur_pos[1] - 1))
        elif action == "up-right":
            swap(map, self.cur_pos, (self.cur_pos[0] - 1, self.cur_pos[1] + 1))
        elif action == "down-left":
            swap(map, self.cur_pos, (self.cur_pos[0] + 1, self.cur_pos[1] - 1))
        elif action == "down-right":
           swap(map, self.cur_pos, (self.cur_pos[0] + 1, self.cur_pos[1] + 1))
            
    def move(map: list[list[int]], action: str) -> bool:
        seeker_current_pos = get_current_pos(map, 3)
        if action == "up":
            swap(map, seeker_current_pos, (seeker_current_pos[0] - 1, seeker_current_pos[1]))
        elif action == "down":
            swap(map, seeker_current_pos, (seeker_current_pos[0] + 1, seeker_current_pos[1]))
        elif action == "left":
            swap(map, seeker_current_pos, (seeker_current_pos[0], seeker_current_pos[1] - 1))
        elif action == "right":
            swap(map, seeker_current_pos, (seeker_current_pos[0], seeker_current_pos[1] + 1))
        elif action == "up-left":
            swap(map, seeker_current_pos, (seeker_current_pos[0] - 1, seeker_current_pos[1] - 1))
        elif action == "up-right":
            swap(map, seeker_current_pos, (seeker_current_pos[0] - 1, seeker_current_pos[1] + 1))
        elif action == "down-left":
            swap(map, seeker_current_pos, (seeker_current_pos[0] + 1, seeker_current_pos[1] - 1))
        elif action == "down-right":
            swap(map, seeker_current_pos, (seeker_current_pos[0] + 1, seeker_current_pos[1] + 1))
            
    def valid_actions(self, map: list[list[int]], map_width, map_height) -> list[str]:
        actions = []
        if self.cur_pos[0] > 0: # can move up
            if self.cur_pos[1] > 0: # can move left
                if map[self.cur_pos[0] - 1][self.cur_pos[1] - 1] != 1: # not a wall
                    actions.append("up-left")
            if self.cur_pos[1] < (map_width - 1): # can move right
                if map[self.cur_pos[0] - 1][self.cur_pos[1] + 1] != 1: # not a wall
                    actions.append("up-right")
            if map[self.cur_pos[0] - 1][self.cur_pos[1]] != 1: # not a wall
                actions.append("up")
        if self.cur_pos[0] < (map_height - 1): # can move down
            if self.cur_pos[1] > 0: # can move left
                if map[self.cur_pos[0] + 1][self.cur_pos[1] - 1] != 1: # not a wall
                    actions.append("down-left")
            if self.cur_pos[1] < (map_width - 1): # can move right
                if map[self.cur_pos[0] + 1][self.cur_pos[1] + 1] != 1:
                    actions.append("down-right")
            if map[self.cur_pos[0] + 1][self.cur_pos[1]] != 1: # not a wall
                actions.append("down")
        if self.cur_pos[1] > 0: # can move left
            if map[self.cur_pos[0]][self.cur_pos[1] - 1] != 1:
                actions.append("left")
        if self.cur_pos[1] < (map_width - 1): # can move right
            if map[self.cur_pos[0]][self.cur_pos[1] + 1] != 1:
                actions.append("right")
        return actions
    
    def move_to_center(self, map: list[list[int]]) -> bool:
        # move to center and mark every cell in vision range
        # if hider is in vision range, stop moving to center
        center = get_map_center(map)
        while self.cur_pos != center:
            observable = logic_vision(map, self.vision_range, self.cur_pos[1], self.cur_pos[0], len(map), len(map[0]))
            for cell in observable:
                if map[cell[0]][cell[1]] == 2:
                    return cell
                # mark every cell in vision range
                map[cell[0]][cell[1]] = 7
            self.move(map, "up-right")
        return False
    
    def generate(self, map: list[list[int]], map_width, map_height, actions) -> list[Node]:
        # maximum 8 successors
        successors = []
        for action in actions:
            new_map = copy.deepcopy(map)
            self.move(new_map, action)
            new_node = Node(new_map, self, action, self.path_cost + 1)
            new_node.calculate_heuristic()
            successors.append(new_node)
        return successors
        
    def initial_logic(self, map: list[list[int]]):
        if not self.cur_pos == self.start_pos:
            return
        else:
            center = get_map_center(map)
            move_to_center_result = self.move_to_center(map)
            if move_to_center_result: # hider is in vision range whilst moving to center
                # A_star_search(map, self.cur_pos, move_to_center_result)
            else: # hider is not in vision range
                # generate successor with heuristic is number of unobserved cells
                # continue going to the generated successor with the lowest heuristic
                # if hider is in vision range, stop going to the generated successor, instead, go to the hider using A* search
                successors = self.generate(map, len(map[0]), len(map), self.valid_actions(map, len(map[0]), len(map)))
                while True:
                    min_heuristic = float('inf')
                    best_successor = None
                    for successor in successors:
                        if successor.heuristic < min_heuristic:
                            min_heuristic = successor.heuristic
                            best_successor = successor
                    self.move(map, best_successor.action)
                    self.path_cost += 1
                    observable = logic_vision(map, self.vision_range, self.cur_pos[1], self.cur_pos[0], len(map), len(map[0]))
                    for cell in observable:
                        if map[cell[0]][cell[1]] == 2: # hider is in vision range
                            # A_star_search(map, self.cur_pos, cell)
                            break