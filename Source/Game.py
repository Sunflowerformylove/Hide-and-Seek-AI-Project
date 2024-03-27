from Seeker import *
from readMaze import print_maze, read_maze
import time
import pygame
from Graphic import show_maze

WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 10
PAUSE = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

pygame.init()

# Idea: Seeker will move first, then hider will move
# Seeker will explore map according to the highest vision unveiled
# If not seeing any hider, and reaching local maximum, seeker trace to a random cell that has not been observed using A* algorithm
# If seeker sees a hider, seeker will trace to the hider using A* algorithm
# Trace here means seeker use the location given, think of the optimal path to reach that location, and move to the next cell in the path
# Because seeker's map does not have any information about hider, seeker will not be able to trace to the hider directly
# Seeker will only be able to trace to the hider if the hider is in the seeker's vision via shared map information
# The random position could be a dead end, meaning that the seeker will not be able to reach the random position, and will have to choose another random position'
# The random position has a chance to be the hider's position, but the seeker will not know that it is the hider's position
# until the hider is in the seeker's vision via shared map information

class Game:
    def __init__(self, filename: str):
        self.maze, self.MAP_DIMENSIONS = read_maze(filename)
        self.seeker = Seeker(self.maze, 0)
        self.hiders = self.set_hiders()

    def set_hiders(self):
        hiders = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 2:
                    hiders.append(Hider(self.maze, 0, (i, j)))
        return hiders
    
    def level_1(self):
        vision = logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
        self.seeker.format_map_by_vision(vision)
        self.seeker.calculate_heuristic_vision()
        turn = False # Seeker moves first
        random_pos = None
        A_star_res = None
        path_to_hider = None
        while running:
            if not turn:
                # print("Seeker's turn")
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    if path_to_hider == None:
                        path_to_hider = self.seeker.trace_random(self.maze, self.MAP_DIMENSIONS, hider_pos)
                        path_to_hider.pop(0)
                        successor = self.seeker.move_to_pos(self.maze, self.MAP_DIMENSIONS, path_to_hider[0])
                        swap(self.maze, self.seeker.current_pos, path_to_hider[0])
                        self.seeker = successor
                        path_to_hider.pop(0)
                    else:
                        successor = self.seeker.move_to_pos(self.maze, self.MAP_DIMENSIONS, path_to_hider[0])
                        swap(self.maze, self.seeker.current_pos, path_to_hider[0])
                        self.seeker = successor
                        path_to_hider.pop(0)
                        if len(path_to_hider) == 0:
                            path_to_hider = None
                    # self.seeker.reset_known_map()
                    # successor = self.seeker.trace_hider(self.maze, self.MAP_DIMENSIONS, hider_pos)
                    # self.seeker = successor
                    if self.seeker.caught_hider(self.hiders):
                        # print_maze(self.maze)
                        show_maze(self.maze)
                        pygame.display.flip()
                        # print("Seeker wins!")
                        break
                elif random_pos != None:
                    # print("Random pos: ", random_pos, "Current pos: ", self.seeker.current_pos)
                    if A_star_res == None:
                        # print(self.seeker.trace_random(self.maze, self.MAP_DIMENSIONS, random_pos))
                        A_star_res = self.seeker.trace_random(self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None: # case of choosing a dead end unobserved cell, for example, cells locked by walls
                            random_pos = None
                            continue
                        A_star_res.pop(0)
                        successor = self.seeker.move_to_pos(self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        A_star_res.pop(0)
                    else:
                        successor = self.seeker.move_to_pos(self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        self.seeker.format_map_by_vision(logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1]))
                        A_star_res.pop(0)
                        if len(A_star_res) == 0:
                            A_star_res = None
                            random_pos = None
                else:
                    successor = self.seeker.move(self.maze, self.MAP_DIMENSIONS)
                    if type(successor) == tuple:
                        # reach local maximum
                        random_pos = successor
                    else:
                        self.seeker = successor
                turn = True
            else:
                # print("Hider's turn")
                for i in range(len(self.hiders)):
                    move = self.hiders[i].move(self.maze, self.MAP_DIMENSIONS, 1)
                    self.hiders[i] = move
                turn = False
            # print_maze(self.maze)
            # time.sleep(1)
            screen.fill((255, 255, 255))
            vision = logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            show_maze(show_map)
            # print_maze(self.seeker.map)
            pygame.display.flip()
            clock.tick(15)
            
    def level_2(self, num_hiders: int):
        pass
        
game = Game("Tests/maze.txt")
game.level_1()
# print(game.seeker.current_pos)
# print(game.MAP_DIMENSIONS)