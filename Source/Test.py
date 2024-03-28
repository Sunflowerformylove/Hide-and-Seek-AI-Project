from Seeker import *
from readMaze import print_maze, read_maze
import time

filename = "Tests/maze.txt"
maze, MAP_DIMENSIONS = read_maze(filename)

def check_map_colored(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] != 4 and maze[i][j] != 3 and maze[i][j] != 2:
                return False
    return True

seeker = Seeker(maze, 0)
print(logic_vision(maze, 3, seeker.current_pos[0], seeker.current_pos[1], MAP_DIMENSIONS[0], MAP_DIMENSIONS[1]))