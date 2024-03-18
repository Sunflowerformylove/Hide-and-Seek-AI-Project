from Support import *
# from Seeker import *
import copy

maze = []
file = open("maze.txt", "r")
for line in file:
    temp = []
    for char in line:
        if char != "\n" and char != " ":
            temp.append(int(char))
    maze.append(temp)

# cur_pos = (0, 0)
# vision_range = 3

def swap(map: list[list[int]], pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    map[pos1[0]][pos1[1]], map[pos2[0]][pos2[1]] = map[pos2[0]][pos2[1]], map[pos1[0]][pos1[1]]
    
def get_map_center(map: list[list[int]]) -> tuple[int, int]:
    return (len(map) // 2, len(map[0]) // 2)

def get_current_pos(map: list[list[int]], agent: int) -> tuple[int, int]:
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == agent:
                return (i, j)

def move(map: list[list[int]], action: str) -> bool:
    seeker_current_pos = get_current_pos(map, 3)
    print(seeker_current_pos)
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

def move_to_center(map: list[list[int]]) -> bool:
    # move to center and mark every cell in vision range
    # if hider is in vision range, stop moving to center
    center = get_map_center(map)
    cur_pos = get_current_pos(map, 3)
    while cur_pos != center:
        # observable = logic_vision(map, vision_range, cur_pos[1], cur_pos[0], len(map), len(map[0]))
        # for cell in observable:
        #     if map[cell[0]][cell[1]] == 2:
        #         return cell
            # mark every cell in vision range
            # map[cell[0]][cell[1]] = 7
        move(map, "up-right")
        cur_pos = get_current_pos(map, 3)       
        for row in maze:
            for cell in row:
                print(cell, end=" ")
            print()
    return False

def generate(map: list[list[int]], map_width, map_height, actions) -> list[Node]:
    # maximum 8 successors
    successors = []
    for action in actions:
        new_map = copy.deepcopy(map)
        move(new_map, action)
        new_node = Node(new_map, self, action, path_cost + 1)
        new_node.calculate_heuristic()
        successors.append(new_node)
    return successors

# # print(move_to_center(maze))
# move_to_center(maze)

vision = logic_vision(maze, 3, 0, 0, len(maze), len(maze[0]))

# for vis in vision:
#     maze[vis[0]][vis[1]] = 8

# move(maze, "right")
# move_to_center(maze)