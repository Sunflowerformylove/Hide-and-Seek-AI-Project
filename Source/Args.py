import sys
import Global
import Graphic
import Game
import random
import importlib
import os

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

def get_file_names():
    Tests_path = os.path.join(os.getcwd(), "Tests")
    filename_pool = os.listdir(Tests_path)
    return filename_pool

def change_global_vars(args):
    global MODE, WIDTH, HEIGHT, LEVEL, FILENAME, FPS, ITERATION, RUN_MODE
    for key, value in args.items():
        if key == "MODE":
            MODE = value
            if MODE == "RANDOM":
                MODE = random.choice(["DARK", "LIGHT", "DUNE"])
        if key == "WIDTH":
            WIDTH = int(value)
        if key == "HEIGHT":
            HEIGHT = int(value)
        if key == "LEVEL":
            LEVEL = value
            if LEVEL == "RANDOM":
                LEVEL = random.choice(["1", "2", "3"])
        if key == "FILENAME":
            FILENAME = value
            if FILENAME == "RANDOM":
                FILENAME = "Tests/" + random.choice(get_file_names())
        if key == "FPS":
            FPS = int(value)
        if key == "ITERATION":
            ITERATION = int(value)
            if ITERATION <= 0:
                ITERATION = random.randint(1, 1000)
        if key == "RUN_MODE":
            RUN_MODE = value
    importlib.reload(Global)
    importlib.reload(Graphic)
    importlib.reload(Game)
    importlib.invalidate_caches()