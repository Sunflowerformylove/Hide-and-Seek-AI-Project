from readMaze import read_maze, print_maze
from Seeker import *
# from readMaze import unobservable_cells
# from Support import logic_vision

MAP_DIMENSION = (7,7)


filename = "maze.txt"
maze = read_maze(filename)
seeker = Seeker(maze, 3, 0, None)
path1 = seeker.move(MAP_DIMENSION)
# print(path1)
path2 = seeker.trace_hider(MAP_DIMENSION, path1[1], path1[0], len(path1[1]))
trace = backtrace(path2)

for node in trace:
    print_maze(node)