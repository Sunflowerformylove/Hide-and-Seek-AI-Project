from readMaze import read_maze, print_maze
from Seeker import *
from readMaze import unobservable_cells

MAP_DIMENSIONS = (8,11)

maze = read_maze("maze.txt")
unobserved = unobservable_cells(maze, (0,5), 3, MAP_DIMENSIONS)
print(unobserved)
vision = vision_logic(maze, (0, 5), 3, MAP_DIMENSIONS)
for row in vision:
    if maze[row[0]][row[1]] == 0:
        maze[row[0]][row[1]] = 4
print_maze(maze)
# print(len(maze), len(maze[0]))
# seeker = Seeker(maze, 3, 0, None)
# path1 = seeker.move((len(maze), len(maze[0])))
# path2 = seeker.trace_hider(MAP_DIMENSIONS, (0,10), path1[0])
# path = backtrace(path2)

# for node in path:
#     print_maze(node)