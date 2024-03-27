def print_maze(maze: list[list[int]])->None:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end = " ")
        print()
    print()

def read_maze(filename: str) -> list[list[int]]:
    maze = []
    file = open(filename, "r")
    line = file.readline().split()
    map_dimensions = [int(line[0]), int(line[1])]
    for line in file:
        temp = []
        for char in line:
            if char != "\n" and char != " ":
                temp.append(int(char))
        maze.append(temp)
    return (maze, map_dimensions)