from Args import *
from Graphic import *
from Game import *
from Global import *
from readMaze import *
import os

def main():
    change_global_vars(get_args())
    game = Game()
    game.run()
    # game.display()

if __name__ == "__main__":
    main()