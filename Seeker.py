from readMaze import is_not_wall
import copy
from Support import PriorityQueue, logic_vision
import time # for debugging purposes

# 1 for wall
# 2 for hider
# 3 for seeker
# 0 for empty
# 4 for seeker's vision
# 5 for hider's vision
# 6 for announced cell
# 7 for vision blocked cell


def swap(map: list[list[int]], pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    if map[pos1[0]][pos1[1]] == 3 and map[pos2[0]][pos2[1]] == 2:
        map[pos1[0]][pos1[1]] = 3
        map[pos2[0]][pos2[1]] = 4
    elif map[pos1[0]][pos1[1]] == 2 and map[pos2[0]][pos2[1]] == 3:
        map[pos1[0]][pos1[1]] = 4
        map[pos2[0]][pos2[1]] = 3
    map[pos1[0]][pos1[1]], map[pos2[0]][pos2[1]
                                        ] = map[pos2[0]][pos2[1]], map[pos1[0]][pos1[1]]


class Seeker:
    def __init__(self, map: list[list[int]], vision_range: int, path_cost: int, parent: "Seeker") -> None:
        self.map: list[list[int]] = map
        self.vision_range = vision_range
        self.center = self.get_map_center()
        self.current_pos = self.get_current_pos(3)
        self.path_cost = path_cost
        self.heuristic = 0
        self.parent = parent

    def get_map_center(self) -> tuple[int, int]:
        return (len(self.map) // 2, len(self.map[0]) // 2)

    def get_current_pos(self, agent: int) -> tuple[int, int]:
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == agent:
                    return (i, j)

    def valid_actions(self, map_dimensions: tuple[int, int]) -> list[str]:
        valid_actions = []
        if self.current_pos[0] > 0:  # if not at the topmost
            # if not at the rightmost
            if (self.current_pos[1] < (map_dimensions[1] - 1)) and is_not_wall(self.map, self.current_pos[0] - 1, self.current_pos[1] + 1):
                valid_actions.append("up-right")
            # if not at the leftmost
            if self.current_pos[1] > 0 and is_not_wall(self.map, self.current_pos[0] - 1, self.current_pos[1] - 1):
                valid_actions.append("up-left")
            if is_not_wall(self.map, self.current_pos[0] - 1, self.current_pos[1]):
                valid_actions.append("up")
        if self.current_pos[0] < map_dimensions[0] - 1:  # if not at the bottommost
            # if not at the rightmost
            if self.current_pos[1] < map_dimensions[1] - 1 and is_not_wall(self.map, self.current_pos[0] + 1, self.current_pos[1] + 1):
                valid_actions.append("down-right")
            # if not at the leftmost
            if self.current_pos[1] > 0 and is_not_wall(self.map, self.current_pos[0] + 1, self.current_pos[1] - 1):
                valid_actions.append("down-left")
            if is_not_wall(self.map, self.current_pos[0] + 1, self.current_pos[1]):
                valid_actions.append("down")
        # if not at the rightmost
        if self.current_pos[1] < map_dimensions[1] - 1 and is_not_wall(self.map, self.current_pos[0], self.current_pos[1] + 1):
            valid_actions.append("right")
        # if not at the leftmost
        if self.current_pos[1] > 0 and is_not_wall(self.map, self.current_pos[0], self.current_pos[1] - 1):
            valid_actions.append("left")
        # priority: up-right, up-left, up, down-right, down-left, down, right, left
        return valid_actions

    def generation(self, map_dimensions: tuple[int, int]):
        successors = []
        for action in self.valid_actions(map_dimensions):
            new_map = copy.deepcopy(self.map)
            if action == "up":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] - 1, self.current_pos[1]))
            elif action == "down":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] + 1, self.current_pos[1]))
            elif action == "left":
                swap(new_map, self.current_pos,
                     (self.current_pos[0], self.current_pos[1] - 1))
            elif action == "right":
                swap(new_map, self.current_pos,
                     (self.current_pos[0], self.current_pos[1] + 1))
            elif action == "up-left":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] - 1, self.current_pos[1] - 1))
            elif action == "up-right":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] - 1, self.current_pos[1] + 1))
            elif action == "down-left":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] + 1, self.current_pos[1] - 1))
            elif action == "down-right":
                swap(new_map, self.current_pos,
                     (self.current_pos[0] + 1, self.current_pos[1] + 1))
            new_seeker = Seeker(new_map, self.vision_range,
                                self.path_cost + 1, self)
            successors.append(new_seeker)
        return successors

    def calculate_heuristic_vision(self) -> int:
        heuristic = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 0:
                    heuristic += 1  # minimum number of unobserved cells
        self.heuristic = heuristic

    def calculate_heuristic_manhattan(self, goalX, goalY) -> int:
        heuristic = abs(self.current_pos[0] - goalX) + \
            abs(self.current_pos[1] - goalY)
        self.heuristic = heuristic
        
    def format_map_by_vision(self, vision: list[tuple]) -> list[list[int]]:
        for cell in vision:
            if self.map[cell[0]][cell[1]] != 2 and self.map[cell[0]][cell[1]] != 3 and self.map[cell[0]][cell[1]] != 1:
                self.map[cell[0]][cell[1]] = 4

    def move(self, map_dimensions: tuple[int, int]) -> bool:
        frontier = PriorityQueue()
        frontier.push(self, 0)
        visited = {tuple(map(tuple, self.map)): 0}
        hiders_pos = []
        while not frontier.empty():
            current = frontier.pop()
            current_pos = current.get_current_pos(3)
            # print("Current position: ", current_pos)
            visible_cells = logic_vision(current.map, current.vision_range, current_pos[0], current_pos[1], map_dimensions[0], map_dimensions[1])
            for cell in visible_cells:
                if current.map[cell[0]][cell[1]] != 2 and current.map[cell[0]][cell[1]] != 3 and current.map[cell[0]][cell[1]] != 1:
                    current.map[cell[0]][cell[1]] = 4
                elif current.map[cell[0]][cell[1]] == 2:
                    hiders_pos.append((cell[0], cell[1]))
                    return (current, hiders_pos)
            # print_maze(current.map)
            # time.sleep(2)
            successors = current.generation(map_dimensions)
            for successor in successors:
                successor_tuple_map = tuple(map(tuple, successor.map))
                if successor_tuple_map not in visited or visited[successor_tuple_map] > successor.path_cost:
                    visited[successor_tuple_map] = successor.path_cost
                    successor.calculate_heuristic_vision()
                    frontier.push(
                        successor, successor.path_cost + successor.heuristic)
        return False
    
    def reached_hider(self, hider_pos: tuple[int, int]) -> bool:
        return self.current_pos == hider_pos

    def trace_hider(self, map_dimensions: tuple[int, int], hider_pos: tuple[int, int], last_node: "Seeker") -> list[list[int]]:
        frontier = PriorityQueue()
        frontier.push(last_node, last_node.calculate_heuristic_manhattan(hider_pos[0], hider_pos[1]))
        visited = {tuple(map(tuple, self.map)): 0}
        while not frontier.empty():
            current = frontier.pop()
            if current.reached_hider(hider_pos):
                return current
            current_pos = current.get_current_pos(3)
            visible_cells = logic_vision(current.map, current.vision_range, current_pos[0], current_pos[1], map_dimensions[0], map_dimensions[1])
            for cell in visible_cells:
                if current.map[cell[0]][cell[1]] != 2 and current.map[cell[0]][cell[1]] != 3 and current.map[cell[0]][cell[1]] != 1:
                    current.map[cell[0]][cell[1]] = 4
            successors = current.generation(map_dimensions)
            for successor in successors:
                successor_tuple_map = tuple(map(tuple, successor.map))
                if successor_tuple_map not in visited or visited[successor_tuple_map] > successor.path_cost:
                    visited[successor_tuple_map] = successor.path_cost
                    successor.calculate_heuristic_manhattan(
                        hider_pos[0], hider_pos[1])
                    frontier.push(
                        successor, successor.path_cost + successor.heuristic)

    def __lt__(self, other: "Seeker"):
        if self.heuristic == other.heuristic:
            return self.path_cost < other.path_cost
        return (self.heuristic + self.path_cost) < (other.heuristic + other.path_cost)


def backtrace(node: Seeker) -> list[list[int]]:
    path = []
    while node:
        path.append(node.map)
        node = node.parent
    return path[::-1]
