from Support import *
from Seeker import *
import copy

maze = []
file = open("maze.txt", "r")
for line in file:
    temp = []
    for char in line:
        if char != "\n" and char != " ":
            temp.append(int(char))
    maze.append(temp)
    
def print_maze(maze):
    for row in maze:
        for cell in row:
            print(cell, end = " ")
        print()

seeker = Seeker(maze, 3, 0, None)
# vision = logic_vision(maze, 3, seeker.current_pos[0], seeker.current_pos[1], len(maze), len(maze[0]))

# print_maze(maze)
(move_result, hider_pos)= seeker.move_to_center((7,7))
path1 = backtrace(move_result)
# for node in path1:
#     print_maze(node)
#     print()
print("Move to center end, hider position: ", hider_pos)
trace = seeker.trace_hider((7,7), hider_pos, move_result)
path2 = backtrace(trace)

for node in path2:
    print_maze(node)
    print()