import sys
import Global
import Graphic
import Game
import random
import importlib
import os
import math
import time
from GenMap import generate_map_randomly, Map

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
            elif FILENAME == "CREATE":
                width = random.randint(10, 100)
                height = random.randint(10, 100)
                num_hiders = math.floor(max(width, height) / 10)
                date = time.strftime("%d_%m_%Y_%H_%M_%S")
                type_map = random.choice([1, 2])
                new_map = generate_map_randomly(width, height, num_hiders, type_map)
                FILENAME = "Tests/" + f"map_{width}_{height}_{num_hiders}_{date}.txt"
                new_map.export_map(FILENAME)
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