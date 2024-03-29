def print_maze(maze: list[list[int]])->None:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end = " ")
        print()
    print()
    
def format_object_to_map(object: list[int], maze: list[list[int]]) -> list[list[int]]:
    # top left, bottom right
    for i in range(object[0], object[2] + 1): # top to bottom
        for j in range(object[1], object[3] + 1): # left to right
            maze[i][j] = 1

def read_maze(filename: str) -> list[list[int]]:
    maze = []
    file = open(filename, "r")
    line = file.readline().split()
    map_dimensions = [int(line[0]), int(line[1])]
    for i in range(map_dimensions[0]):
        line = file.readline().split()
        temp = []
        for char in line:
            if char != "\n" and char != " ":
                temp.append(int(char))
        maze.append(temp)
    for line in file:
        line.strip("\n")
        line = line.split(" ")
        object = []
        for char in line:
            if char != "\n" and char != " ":
                object.append(int(char))
        format_object_to_map(object, maze)    
    return (maze, map_dimensions)