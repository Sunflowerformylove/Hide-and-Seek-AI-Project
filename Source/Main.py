from Args import *
from Graphic import *
from Game import *
from Global import *

def main():
    change_global_vars(get_args())
    game = Game()
    game.run()
if __name__ == "__main__":
    main()