def print_maze(maze: list[list[int]])->None:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end = " ")
        print()
    print()
    
# a lot of if else statements, but it works
def unobservable_cells(maze: list[list[int]], seeker_pos: tuple[int,int], vision_range: int, map_dimension: tuple[int, int]) -> list[tuple[int,int]]:
    # first, vertical, horizontal, and diagonal vision
    # horizontal vision, block in T shape
    unobservable = []
    for i in range(seeker_pos[1] - vision_range, seeker_pos[1] + vision_range + 1):
        if i >= 0 and (i < map_dimension[0]) and maze[seeker_pos[0]][i] == 1:
            if i < seeker_pos[1]: # left
                for j in range(seeker_pos[1] - vision_range, i):
                    if j >= 0 and maze[seeker_pos[0]][j] == 0:
                        unobservable.append((seeker_pos[0], j))
                    if j >= 0 and j == (i - vision_range + 1):
                        if seeker_pos[0] >= 1:
                            unobservable.append((seeker_pos[0] - 1, j))
                        if seeker_pos[0] < (map_dimension[0] - 1):
                            unobservable.append((seeker_pos[0] + 1, j))
            else: # right
                for j in range(i + 1, seeker_pos[1] + vision_range + 1):
                    if maze[seeker_pos[0]][j] == 0:
                        unobservable.append((seeker_pos[0], j))
                    if j >= 0 and j == (i + vision_range - 1):
                        if seeker_pos[0] >= 1:
                            unobservable.append((seeker_pos[0] - 1, j))
                        if seeker_pos[0] < (map_dimension[0] - 1):
                            unobservable.append((seeker_pos[0] + 1, j))
    # vertical vision, also block in T shape
    for i in range(seeker_pos[0] - vision_range, seeker_pos[0] + vision_range + 1):
        if (i >= 0) and (i < map_dimension[0]) and maze[i][seeker_pos[1]] == 1:
            if i < seeker_pos[0]: # up
                for j in range(seeker_pos[0] - vision_range, i):
                    if j >= 0 and maze[j][seeker_pos[1]] == 0:
                        unobservable.append((j, seeker_pos[1]))
                    if j >= 0 and j == (i - vision_range + 1):
                        if seeker_pos[1] >= 1:
                            unobservable.append((j, seeker_pos[1] - 1))
                        if seeker_pos[1] < (map_dimension[1] - 1):
                            unobservable.append((j, seeker_pos[1] + 1))
            else: # down
                for j in range(i + 1, seeker_pos[0] + vision_range + 1):
                    if maze[j][seeker_pos[1]] == 0:
                        unobservable.append((j, seeker_pos[1]))
                    if j >= 0 and j == (i + vision_range - 1):
                        if seeker_pos[1] >= 1:
                            unobservable.append((j, seeker_pos[1] - 1))
                        if seeker_pos[1] < (map_dimension[1] - 1):
                            unobservable.append((j, seeker_pos[1] + 1))
    # diagonal vision
    for i in range(seeker_pos[0] - vision_range, seeker_pos[0] + vision_range + 1):
        for j in range(seeker_pos[1] - vision_range, seeker_pos[1] + vision_range + 1):
            if i >= 0 and i < map_dimension[0] and j >= 0 and j < map_dimension[1]:
                if abs(i - seeker_pos[0]) == abs(j - seeker_pos[1]):
                    if maze[i][j] == 1:
                        if (i < seeker_pos[0]) and (j < seeker_pos[1]): # top left
                            # if 1 and 2 are walls, block 5, if 2 and 3 are walls, block 7
                            if (abs(i - seeker_pos[0]) == 1) and (abs(j - seeker_pos[1]) == 1): #2
                                if(maze[i][j + 1] == 1): #1
                                    unobservable.append((i - 1, j))
                                if (maze[i + 1][j] == 8): #3
                                    unobservable.append((i, j - 1))
                                one_level = (i - 1, j - 1)
                                if one_level[1] >= 1:
                                    unobservable.append((one_level[0], one_level[1] - 1))
                                if one_level[0] >= 1:
                                    unobservable.append((one_level[0] - 1, one_level[1]))
                            for k in range(1, vision_range):
                                if (i - k) >= 0 and (j - k) >= 0 and maze[i - k][j - k] == 0:
                                    unobservable.append((i - k, j - k))
                        elif (i < seeker_pos[0]) and (j > seeker_pos[1]): # top right
                            if (abs(i - seeker_pos[0]) == 1) and (abs(j - seeker_pos[1]) == 1):
                                if(maze[i][j - 1] == 1): #1
                                    unobservable.append((i - 1, j))
                                if (maze[i + 1][j] == 1): #3
                                    unobservable.append((i, j + 1))
                                one_level = (i - 1, j + 1)
                                if one_level[1] < (map_dimension[1] - 1):
                                    unobservable.append((one_level[0], one_level[1] + 1))
                                if one_level[0] >= 1:
                                    unobservable.append((one_level[0] - 1, one_level[1]))
                            for k in range(1, vision_range):
                                if (i - k) >= 0 and (j + k) < map_dimension[1] and maze[i - k][j + k] == 0:
                                    unobservable.append((i - k, j + k))
                        elif (i > seeker_pos[0]) and (j < seeker_pos[1]): # bottom left
                            if (abs(i - seeker_pos[0]) == 1) and (abs(j - seeker_pos[1]) == 1):
                                if (maze[i][j + 1] == 1): #1
                                    unobservable.append((i + 1, j))
                                if (maze[i - 1][j] == 1): #3
                                    unobservable.append((i, j - 1))
                                one_level = (i + 1, j - 1)
                                if one_level[1] >= 1:
                                    unobservable.append((one_level[0], one_level[1] - 1))
                                if one_level[0] < (map_dimension[0] - 1):
                                    unobservable.append((one_level[0] + 1, one_level[1]))
                            for k in range(1, vision_range):
                                if (i + k) < map_dimension[0] and (j - k) >= 0 and maze[i + k][j - k] == 0:
                                    unobservable.append((i + k, j - k))
                        else: # bottom right    
                            if (abs(i - seeker_pos[0]) == 1) and (abs(j - seeker_pos[1]) == 1):
                                if (maze[i][j - 1] == 1): #1
                                    unobservable.append((i + 1, j))
                                if (maze[i - 1][j] == 1): #3
                                    unobservable.append((i, j + 1))
                                one_level = (i + 1, j + 1)
                                if one_level[1] < (map_dimension[1] - 1):
                                    unobservable.append((one_level[0], one_level[1] + 1))
                                if one_level[0] < (map_dimension[0] - 1):
                                    unobservable.append((one_level[0] + 1, one_level[1]))
                            for k in range(1, vision_range):
                                if (i + k) < map_dimension[0] and (j + k) < map_dimension[1] and maze[i + k][j + k] == 0:
                                    unobservable.append((i + k, j + k))
                                    
    for i in range(seeker_pos[1] - vision_range, seeker_pos[1] + vision_range + 1):
        for j in range(seeker_pos[0] - vision_range, seeker_pos[0] + vision_range + 1):
            if i >= 0 and i < map_dimension[0] and j >= 0 and j < map_dimension[1]:
                if abs(i - seeker_pos[0]) == abs(j - seeker_pos[1]):
                    if (i >= 1) and (maze[i - 1][j] == 1): # 5 is wall
                            if (i < seeker_pos[0]) and (j < seeker_pos[1]): # top left
                                unobservable.append((i - 2, j))
                                unobservable.append((i - 2, j - 1))
                            elif (i < seeker_pos[0]) and (j > seeker_pos[1]): # top right
                                unobservable.append((i - 2, j))
                                unobservable.append((i - 2, j + 1))
                    if (i < map_dimension[0] - 1) and i <= (maze[i + 1][j] == 1): # 5 is wall
                        if (i > seeker_pos[0]) and (j < seeker_pos[1]): # bottom left
                            unobservable.append((i + 2, j))
                            unobservable.append((i + 2, j - 1))
                        elif (i > seeker_pos[0]) and (j > seeker_pos[1]): # bottom right
                            unobservable.append((i + 2, j))
                            unobservable.append((i + 2, j + 1))
                    if (j >= 1) and (maze[i][j - 1] == 1): # 7 is wall
                        if (i < seeker_pos[0]) and (j < seeker_pos[1]): # top left
                            unobservable.append((i, j - 2))
                            unobservable.append((i - 1, j - 2))
                        elif (i > seeker_pos[0]) and (j < seeker_pos[1]): # bottom left
                            unobservable.append((i, j - 2))
                            unobservable.append((i + 1, j - 2))
                    if (j < map_dimension[1] - 1) and (maze[i][j + 1] == 1): # 7 is wall
                        if (i < seeker_pos[0]) and (j > seeker_pos[1]): # top right
                            unobservable.append((i, j + 2))
                            unobservable.append((i - 1, j + 2))
                        elif (i > seeker_pos[0]) and (j > seeker_pos[1]): # bottom right
                            unobservable.append((i, j + 2))
                            unobservable.append((i + 1, j + 2))
    return unobservable

def read_maze(filename: str) -> list[list[int]]:
    maze = []
    file = open(filename, "r")
    line = file.readline().split()
    # MAP_DIMENSIONS = (int(line[0]), int(line[1]))
    for line in file:
        temp = []
        for char in line:
            if char != "\n" and char != " ":
                temp.append(int(char))
        maze.append(temp)
    return maze

def observable_cells(maze: list[list[int]], seeker_pos: tuple[int,int], vision_range: int, unobservable: list[tuple[int,int]], map_dimension) -> list[tuple[int,int]]:
    visible = []
    for i in range(seeker_pos[0] - vision_range, seeker_pos[0] + vision_range + 1):
        for j in range(seeker_pos[1] - vision_range, seeker_pos[1] + vision_range + 1):
            if i >= 0 and i < map_dimension[0] and j >= 0 and j < map_dimension[1]:
                if (i,j) not in unobservable and (maze[i][j] == 0 or maze[i][j] == 2):
                    visible.append((i,j))
    return visible

def vision_logic(maze: list[list[int]], seeker_pos: tuple[int,int], vision_range: int, map_dimension) -> list[tuple[int,int]]:
    unobservable = unobservable_cells(maze, seeker_pos, vision_range, map_dimension)
    observable = observable_cells(maze, seeker_pos, vision_range, unobservable, map_dimension)
    return observable

def is_not_wall(maze: list[list[int]], i: int, j: int) -> bool:
    return maze[i][j] != 1

def test(maze, seeker_pos,vision_range,map_dimension):
    sevens = [(seeker_pos[0] - 1, seeker_pos[1] - 2),
            (seeker_pos[0] - 1, seeker_pos[1] + 2),
            (seeker_pos[0] + 1, seeker_pos[1] - 2),
            (seeker_pos[0] + 1, seeker_pos[1] + 2) 
            ]
    fives = [(seeker_pos[0] - 1, seeker_pos[1] - 2),
            (seeker_pos[0] - 1, seeker_pos[1] + 2),
            (seeker_pos[0] + 1, seeker_pos[1] - 2),
            (seeker_pos[0] + 1, seeker_pos[1] + 2) 
            ]
    unobservable = []
    for seven in sevens:
        if seven[0] >= 0 and seven[0] < map_dimension[0] and seven[1] >= 0 and seven[1] < map_dimension[1]:
            if maze[seven[0]][seven[1]] == 1:
                # top left
                if seven[0] < seeker_pos[0] and seven[1] < seeker_pos[1]:
                        unobservable.append((seven[0], seven[1] - 1))
                        unobservable.append((seven[0] - 1, seven[1] - 1))
                # top right
                if seven[0] < seeker_pos[0] and seven[1] > seeker_pos[1]:
                        unobservable.append((seven[0], seven[1] + 1))
                        unobservable.append((seven[0] - 1, seven[1] + 1))
                # bottom left
                if seven[0] > seeker_pos[0] and seven[1] < seeker_pos[1]:
                        unobservable.append((seven[0], seven[1] - 1))
                        unobservable.append((seven[0] + 1, seven[1] - 1))
                # bottom right
                if seven[0] > seeker_pos[0] and seven[1] > seeker_pos[1]:
                        unobservable.append((seven[0], seven[1] + 1))
                        unobservable.append((seven[0] + 1, seven[1] + 1))
    for five in fives:
        if five[0] >= 0 and five[0] < map_dimension[0] and five[1] >= 0 and five[1] < map_dimension[1]:
            print(five)
            
            if maze[five[0]][five[1]] == 1:
                # top left
                if five[0] < seeker_pos[0] and five[1] < seeker_pos[1]:
                        unobservable.append((five[0] - 1, five[1]))
                        unobservable.append((five[0] - 1, five[1] - 1))
                # top right
                if five[0] < seeker_pos[0] and five[1] > seeker_pos[1]:
                        unobservable.append((five[0] - 1, five[1]))
                        unobservable.append((five[0] - 1, five[1] + 1))
                # bottom left
                if five[0] > seeker_pos[0] and five[1] < seeker_pos[1]:
                        unobservable.append((five[0] + 1, five[1]))
                        unobservable.append((five[0] + 1, five[1] - 1))
                # bottom right
                if five[0] > seeker_pos[0] and five[1] > seeker_pos[1]:
                        unobservable.append((five[0] + 1, five[1]))
                        unobservable.append((five[0] + 1, five[1] + 1))
    return unobservable


filename = "maze.txt"
maze = read_maze(filename)
# observable = vision_logic(maze, (1,4), 3, (8,11))
unobservable = test(maze, (0,5), 3, (8,11))
print(unobservable)
observable = observable_cells(maze, (0,5), 3, unobservable, (8,11))
for cell in observable:
    maze[cell[0]][cell[1]] = 4
    
print_maze(maze)
