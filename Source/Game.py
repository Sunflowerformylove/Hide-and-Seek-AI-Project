from Seeker import *
from readMaze import print_maze, read_maze
import time
import pygame
from Graphic import *

pygame.init()
running = True

# Idea: Seeker will move first, then hider will move
# Seeker will explore map according to the highest vision unveiled
# If not seeing any hider, and reaching local maximum, seeker trace to a random cell that has not been observed using A* algorithm
# If seeker sees a hider, seeker will trace to the hider using A* algorithm
# Trace here means seeker use the location given, think of the optimal path to reach that location, and move to the next cell in the path
# Because seeker's map does not have any information about hider, seeker will not be able to trace to the hider directly
# Seeker will only be able to trace to the hider if the hider is in the seeker's vision via shared map information
# The random position could be a dead end, meaning that the seeker will not be able to reach the random position, and will have to choose another random position'
# The random position has a chance to be the hider's position, but the seeker will not know that it is the hider's position
# until the hider is in the seeker's vision 

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
        while running:
            if not turn:
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    successor = self.seeker.trace_hider(self.maze, self.MAP_DIMENSIONS, hider_pos)
                    self.seeker = successor
                    if self.seeker.caught_hider(self.hiders):
                        winner = pygame.font.Font(None, 36).render("Seeker wins", 1, (255, 0, 0))
                        screen.blit(winner, (WIDTH - 10, 10))
                        show_maze(self.maze)
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        break
                elif random_pos != None:
                    if A_star_res == None:
                        A_star_res = self.seeker.trace_random(self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None:
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
                        random_pos = successor
                    else:
                        self.seeker = successor
            else:
                for i in range(len(self.hiders)):
                    move = self.hiders[i].move(self.maze, self.MAP_DIMENSIONS, 1)
                    self.hiders[i] = move
            screen.fill((0,0,0))
            vision = logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            handle_event()
            turn_text = pygame.font.Font(None, 36).render("Seeker's turn" if not turn else "Hider's turn", 1, (255, 0, 0))
            screen.blit(turn_text, (10, 10))
            show_maze(show_map)
            pygame.display.flip()
            clock.tick(20)
            turn = not turn
            
    def level_2(self, num_hiders: int):
        vision = logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
        turn = False # Seeker moves first
        random_pos = None
        A_star_res = None
        while running:
            if not turn:
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    successor = self.seeker.trace_hider(self.maze, self.MAP_DIMENSIONS, hider_pos)
                    self.seeker = successor
                    if self.seeker.caught_hider(self.hiders):
                        num_hiders -= 1
                        if num_hiders == 0:
                            winner = pygame.font.Font(None, 36).render("Seeker wins", 1, (255, 0, 0))
                            screen.blit(winner, (WIDTH - winner.get_width() - 10, 10))
                            show_maze(self.maze)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            break
                elif random_pos != None:
                    if A_star_res == None:
                        A_star_res = self.seeker.trace_random(self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None:
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
                        random_pos = successor
                    else:
                        self.seeker = successor
            else:
                for i in range(len(self.hiders)):
                    move = self.hiders[i].move(self.maze, self.MAP_DIMENSIONS, 1)
                    self.hiders[i] = move
            screen.fill((0,0,0))
            vision = logic_vision(self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            handle_event()
            turn_text = pygame.font.Font(None, 36).render("Seeker's turn" if not turn else "Hider's turn", 1, (255, 0, 0))
            screen.blit(turn_text, (10, 10))
            show_maze(show_map)
            pygame.display.flip()
            clock.tick(10)
            turn = not turn

game = Game("Tests/clone.txt")
game.level_2(len(game.hiders))
pygame.quit()