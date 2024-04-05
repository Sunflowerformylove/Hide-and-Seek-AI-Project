import sys
import Global
import Graphic
import Game
# from Global import MODE, WIDTH, HEIGHT, LEVEL, FILENAME, FPS
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
        if key == "FPS":
            FPS = int(value)
        if key == "ITERATION":
            ITERATION = int(value)
    importlib.reload(Global)
    importlib.reload(Graphic)
    importlib.reload(Game)
    importlib.invalidate_caches()