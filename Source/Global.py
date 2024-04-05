# GLOBAL VARIABLES
WIDTH, HEIGHT = 1280, 720
MODE = "DARK"
LEVEL = "3"
CELL_SIZE = 60
FILENAME = "Tests/maze5.txt"
MAZE = []
MAP_DIMENSIONS = (0, 0)
PAUSE = False
SCORE = 0
RUN = 0
FPS = 60
ITERATION = 1
DARK_MODE = {
    'background': (0,0,0), # Outer Space
    'wall': (242, 245, 234), # Ivory
    'hider': (51, 153, 137), # Persian green
    'seeker': (229, 56, 59), # Imperial red
    'observed': (247, 135, 100), # Coral
    'announcement': (157, 180, 171), # Ash grey
    'free': (253, 254, 250), # White-ish
    "object": (150, 205, 255), # Light Sky Blue
    "text": (255, 255, 255) # White
}

LIGHT_MODE = {
    "background": (239, 247, 246), # Mini Cream
    "wall": (6, 7, 14), # Black
    "hider": (161, 229, 171), # Celadon Green
    "seeker": (255, 119, 119), # Pastel Red
    "observed": (188, 150, 230), # Wisteria
    "announcement": (8, 127, 140), # Teal
    "free": (13, 13, 11), # Black-ish
    "object": (131, 188, 255), # Jordy Blue
    "text": (0, 0, 0) # Black
}

DUNE_MODE = {
    "background": (100, 100, 100), # Black
    "wall": (63,78,97), # Grey
    "hider": (33,76,170), # Tory Blue - eyes of Muad'Dib and the Fremen
    "seeker": (224,221,214), # Gainboro - Sardaukar
    "observed": (121,38,6), # Soapstone - Sardaukar's flag
    "announcement": (27,27,29), # Dark Jungle Green - thumper
    "free": (214,152,113), # Burning sand - sand of Arrakis
    "object": (249,254,251), # Burnt orange - Spice Melange
    "text": (255,255,255) # White
}