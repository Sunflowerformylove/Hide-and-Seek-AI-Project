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
seeker.format_map_by_vision(logic_vision(maze, 3, seeker.current_pos[0], seeker.current_pos[1], MAP_DIMENSIONS[0], MAP_DIMENSIONS[1]))
print_maze(seeker.map)
result = seeker.trace_random(maze, MAP_DIMENSIONS, (9,9))

for i in range(len(result)):
    successor = seeker.move_to_pos(maze, MAP_DIMENSIONS, result[i])
    swap(maze, seeker.current_pos, result[i])
    # swap(seeker.map, seeker.current_pos, result[i])
    print(seeker.current_pos, result[i])
    seeker = successor
    print_maze(seeker.map)