import sys
import Global
import Graphic
import Game
import random
import importlib

def get_args():
    args = sys.argv
    if len(args) == 0:
        return {}
    args.pop(0)
    args_dict = {}
    for arg in args:
        key, value = arg.split("=")
        args_dict[key] = value
    return args_dict

def change_global_vars(args):
    global MODE, WIDTH, HEIGHT, LEVEL, FILENAME, FPS, ITERATION
    FILENAME_POOL = ["map1_1.txt", "map1.txt", "map2.txt", "map3.txt", "map4.txt","map5.txt", "maze.txt",
                    "maze1.txt", "maze2.txt", "maze3.txt", "maze4.txt", "maze5.txt", "maze6.txt", "maze7.txt",
                    "maze8.txt", "maze9.txt", "maze10.txt", "maze11.txt", "maze12.txt"]
    for key, value in args.items():
        if key == "MODE":
            MODE = value
        if key == "WIDTH":
            WIDTH = int(value)
        if key == "HEIGHT":
            HEIGHT = int(value)
        if key == "LEVEL":
            LEVEL = value
        if key == "FILENAME":
            FILENAME = value
            if FILENAME == "RANDOM":
                FILENAME = "Tests/" + random.choice(FILENAME_POOL)
        if key == "FPS":
            FPS = int(value)
        if key == "ITERATION":
            ITERATION = int(value)
    importlib.reload(Global)
    importlib.reload(Graphic)
    importlib.reload(Game)
    importlib.invalidate_caches()