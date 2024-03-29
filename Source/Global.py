import sys

# GLOBAL VARIABLES
WIDTH, HEIGHT = 1280, 720
MODE = "dark"
CELL_SIZE = 50
FILENAME = "Test/maze.txt"
MAZE = []
MAP_DIMENSIONS = (0, 0)
PAUSE = False

def exec():
    global WIDTH, HEIGHT, MODE, CELL_SIZE, FILENAME, MAZE, MAP_DIMENSIONS
    args = sys.argv
    args.pop(0) # Remove the first element which is the name of the file
    args_dict = {}
    for i in range(len(args)):
        item, value = args[i].split("=")
        args_dict[item] = value
        
    for key in args_dict:
        if key == "width":
            WIDTH = int(args_dict[key])
        if key == "height":
            HEIGHT = int(args_dict[key])
        if key == "mode":
            MODE = args_dict[key]
        if key == "cell_size":
            CELL_SIZE = int(args_dict[key])
        if key == "filename":
            FILENAME = args_dict[key]
            
    if args_dict.get("filename") is not None:
        with open(FILENAME, "r") as file:
            for line in file:
                MAZE.append([int(i) for i in line.strip()])
            MAP_DIMENSIONS = (len(MAZE[0]), len(MAZE))