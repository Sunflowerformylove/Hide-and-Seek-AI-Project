from Seeker import *
from readMaze import print_maze, read_maze
import time
import pygame
from Global import *
from Graphic import *
from Args import *
import math

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

# Priority of targets will be:
# 1. Hider in vicinity
# 2. Nearest hider's announcement and its vicinity
# 3. Random position
# 4. Local maximum aka sweeping the map

# For level 3 and 4, the priority will be slightly different, as the seeker will have to trace to the last seen position of the hider
# So, last seen pos will be hider than announcement, and announcement will be higher than random position

# Finding either hider or hider's last seen position will effectively clear the known map, as well as the random position
# and its A* path, and the announcement and its A* path

def format_time(seconds: int) -> str:
    hours = "{:02d}".format(int(seconds // 3600))
    minutes = "{:02d}".format(int(seconds // 60))
    seconds = seconds % 60
    seconds = "{:06.3f}".format(seconds) # at least 6 characters, 3 decimal points, 2 digits before decimal point, a dot
    return f"{hours} : {minutes} : {seconds}"

class Game:
    def __init__(self):
        global CELL_SIZE
        global HEIGHT, WIDTH, MODE, FILENAME
        self.maze, self.MAP_DIMENSIONS = read_maze(FILENAME)
        self.seeker = Seeker(self.maze, 0)
        self.hiders = self.set_hiders()
        self.announcements = self.set_announcements()

    def reset(self):
        global SCORE
        self.maze, self.MAP_DIMENSIONS = read_maze(FILENAME)
        self.seeker = Seeker(self.maze, 0)
        self.hiders = self.set_hiders()
        self.announcements = self.set_announcements()
        SCORE = 0

    def set_hiders(self):
        hiders = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 2:
                    hiders.append(Hider(self.maze, 0, (i, j)))
        return hiders

    def set_announcements(self):
        announcements = []
        for i in range(len(self.hiders)):
            announcements.append(None)
        return announcements

    def level_1(self):
        global SCORE
        global FPS
        global RUN
        global MODE, DARK_MODE, LIGHT_MODE, DUNE_MODE
        if MODE == "DARK":
            colors = DARK_MODE
        elif MODE == "LIGHT":
            colors = LIGHT_MODE
        elif MODE == "DUNE":
            colors = DUNE_MODE
        else:
            colors = DARK_MODE
        vision = logic_vision(
            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
        self.seeker.format_map_by_vision(vision)
        self.seeker.calculate_heuristic_vision()
        turn = False  # Seeker moves first
        random_pos = None
        A_star_res = None
        prioritized = None
        A_star_ann = None
        turn_so_far = 0
        while running:
            if not turn:
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(
                    self.maze, self.MAP_DIMENSIONS)
                announce_in_vicinity, ann_pos = self.seeker.announce_in_vicinity(
                    self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    if prioritized != None:
                        A_star_ann = None
                        prioritized = None
                    successor = self.seeker.trace_hider(
                        self.maze, self.MAP_DIMENSIONS, hider_pos, 1)
                    self.seeker = successor
                    if self.seeker.caught_hider(self.hiders, self.maze, self.announcements):
                        SCORE += 20
                        screen.fill(colors["background"])
                        winner = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                            "Seeker wins", 1, colors["text"])
                        screen.blit(winner, (WIDTH - 10, 10))
                        show_maze(self.maze)
                        pygame.display.flip()
                        break
                elif announce_in_vicinity and (prioritized == None or prioritized == []):
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    for i in range(len(self.hiders)):
                        if self.announcements[i] and self.announcements[i].get_pos() == ann_pos:
                            prioritized = self.announcements[i].get_info()
                            break
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                elif A_star_ann != None:
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                    if len(A_star_ann) == 0:
                        A_star_ann = None
                elif A_star_ann == None and prioritized != None and prioritized != []:
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    A_star_ann.pop(0)
                elif random_pos != None:
                    if A_star_res == None:
                        A_star_res = self.seeker.trace_random(
                            self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None:
                            random_pos = None
                            continue
                        A_star_res.pop(0)
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        A_star_res.pop(0)
                    else:
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        self.seeker.format_map_by_vision(logic_vision(
                            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1]))
                        A_star_res.pop(0)
                        if len(A_star_res) == 0:
                            A_star_res = None
                            random_pos = None
                else:
                    successor = self.seeker.move(
                        self.maze, self.MAP_DIMENSIONS)
                    if type(successor) == tuple:
                        random_pos = successor
                    else:
                        self.seeker = successor
                SCORE -= 1
            else:
                turn_so_far += 1
                for i in range(len(self.hiders)):
                    ann_prev_pos = None
                    if self.announcements[i]:
                        ann_prev_pos = self.announcements[i].get_pos()
                    announcement = self.hiders[i].announce(
                        turn_so_far, self.maze, self.MAP_DIMENSIONS)
                    if announcement:
                        self.announcements[i] = announcement
                        ann_pos = announcement.get_pos()
                        if ann_prev_pos and self.maze[ann_prev_pos[0]][ann_prev_pos[1]] == 6:
                            self.maze[ann_prev_pos[0]][ann_prev_pos[1]] = 0
                        self.maze[ann_pos[0]][ann_pos[1]] = 6
                    move = self.hiders[i].move(
                        self.maze, self.MAP_DIMENSIONS, 1)
                    self.hiders[i] = move
                if turn_so_far >= 6:
                    turn_so_far = 0
            screen.fill(colors["background"])
            vision = logic_vision(
                self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            handle_event()
            turn_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Seeker's turn" if not turn else "Hider's turn", 1, colors["text"])
            screen.blit(turn_text, (10, 10))
            score_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Score: " + str(SCORE), 1, colors["text"])
            run_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Run: #" + str(RUN), 1, colors["text"])
            FPS_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "FPS: " + str(math.ceil(clock.get_fps())), 1, colors["text"])
            screen.blit(run_text, (10, HEIGHT - 10 - run_text.get_height()))
            screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))
            screen.blit(FPS_text, (WIDTH - 10 - FPS_text.get_width(), 10))
            show_maze(show_map)
            pygame.display.flip()
            clock.tick(FPS)
            turn = not turn
        RUNE += 1

    def level_2(self, num_hiders: int):
        global SCORE
        global RUN
        global FPS
        global MODE, DARK_MODE, LIGHT_MODE, DUNE_MODE
        if MODE == "DARK":
            colors = DARK_MODE
        elif MODE == "LIGHT":
            colors = LIGHT_MODE
        elif MODE == "DUNE":
            colors = DUNE_MODE
        else:
            colors = DARK_MODE
        vision = logic_vision(
            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
        turn = False  # Seeker moves first
        random_pos = None
        A_star_res = None
        A_star_ann = None
        prioritized = None
        turn_so_far = 0
        while True:
            if not turn:
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(self.maze, self.MAP_DIMENSIONS)
                announce_in_vicinity, ann_pos = self.seeker.announce_in_vicinity(self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    if prioritized != None:
                        A_star_ann = None
                        prioritized = None
                    successor = self.seeker.trace_hider(
                        self.maze, self.MAP_DIMENSIONS, hider_pos, 2)
                    self.seeker = successor
                    if self.seeker.caught_hider(self.hiders, self.maze, self.announcements):
                        num_hiders -= 1
                        SCORE += 20
                        if num_hiders == 0:
                            screen.fill(colors["background"])
                            winner = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                                "Seeker wins", 1, colors["text"])
                            screen.blit(
                                winner, (WIDTH - winner.get_width() - 10, 10))
                            show_maze(self.maze)
                            pygame.display.flip()
                            break
                elif announce_in_vicinity and (prioritized == None or prioritized == []):
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    for i in range(len(self.hiders)):
                        if self.announcements[i] and self.announcements[i].get_pos() == ann_pos:
                            prioritized = self.announcements[i].get_info()
                            break
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                elif A_star_ann != None:
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                    if len(A_star_ann) == 0:
                        A_star_ann = None
                elif A_star_ann == None and prioritized != None and prioritized != []:
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    A_star_ann.pop(0)
                elif random_pos != None:
                    if A_star_res == None:
                        A_star_res = self.seeker.trace_random(
                            self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None:
                            random_pos = None
                            continue
                        A_star_res.pop(0)
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        A_star_res.pop(0)
                    else:
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        self.seeker.format_map_by_vision(logic_vision(
                            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1]))
                        A_star_res.pop(0)
                        if len(A_star_res) == 0:
                            A_star_res = None
                            random_pos = None
                else:
                    successor = self.seeker.move(
                        self.maze, self.MAP_DIMENSIONS)
                    if type(successor) == tuple:
                        random_pos = successor
                    else:
                        self.seeker = successor
                SCORE -= 1
            else:
                turn_so_far += 1
                for i in range(len(self.hiders)):
                    ann_prev_pos = None
                    if self.announcements[i]:
                        ann_prev_pos = self.announcements[i].get_pos()
                    announcement = self.hiders[i].announce(
                        turn_so_far, self.maze, self.MAP_DIMENSIONS)
                    if announcement:
                        self.announcements[i] = None
                        self.announcements[i] = announcement
                        ann_pos = announcement.get_pos()
                        if ann_prev_pos and self.maze[ann_prev_pos[0]][ann_prev_pos[1]] == 6:
                            self.maze[ann_prev_pos[0]][ann_prev_pos[1]] = 0
                        self.maze[ann_pos[0]][ann_pos[1]] = 6
                    move = self.hiders[i].move(
                        self.maze, self.MAP_DIMENSIONS, 2)
                    self.hiders[i] = move
                if turn_so_far >= 6:
                    turn_so_far = 0
            screen.fill(colors["background"])
            vision = logic_vision(
                self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            handle_event()
            turn_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Seeker's turn" if not turn else "Hider's turn", 1, colors["text"])
            screen.blit(turn_text, (10, 10))
            score_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Score: " + str(SCORE), 1, colors["text"])
            FPS_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "FPS: " + str(math.ceil(clock.get_fps())), 1, colors["text"])
            screen.blit(score_text, (WIDTH / 2 - score_text.get_width(), 10))
            run_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Run: #" + str(RUN), 1, colors["text"])
            screen.blit(run_text, (10, HEIGHT - 10 - run_text.get_height()))
            screen.blit(FPS_text, (WIDTH - 10 - FPS_text.get_width(), 10))
            show_maze(show_map)
            pygame.display.flip()
            clock.tick(FPS)
            turn = not turn
        RUN += 1

    def level_3(self, num_hiders: int):
        global SCORE
        global RUN
        global FPS
        global MODE, DARK_MODE, LIGHT_MODE, DUNE_MODE
        if MODE == "DARK":
            colors = DARK_MODE
        elif MODE == "LIGHT":
            colors = LIGHT_MODE
        elif MODE == "DUNE":
            colors = DUNE_MODE
        else:
            colors = DARK_MODE
        vision = logic_vision(
            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
        turn = False  # Seeker moves first
        random_pos = None
        A_star_res = None
        A_star_ann = None
        prioritized = None
        last_seen = None
        turn_so_far = 0
        while running:
            if not turn:
                is_in_vicinity, hider_pos = self.seeker.hider_in_vicinity(
                    self.maze, self.MAP_DIMENSIONS)
                announce_in_vicinity, ann_pos = self.seeker.announce_in_vicinity(
                    self.maze, self.MAP_DIMENSIONS)
                if is_in_vicinity:
                    last_seen = hider_pos
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    if prioritized != None:
                        A_star_ann = None
                        prioritized = None
                    self.seeker.reset_known_map()
                    successor = self.seeker.trace_hider(
                        self.maze, self.MAP_DIMENSIONS, hider_pos, 3)
                    self.seeker = successor
                    if self.seeker.caught_hider(self.hiders, self.maze, self.announcements):
                        last_seen = None
                        SCORE += 20
                        num_hiders -= 1
                        for announcement in self.announcements:
                            if announcement:
                                self.maze[announcement.get_pos()[0]][announcement.get_pos()[1]] = 6
                        if num_hiders == 0:
                            screen.fill(colors["background"])
                            winner = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                                "Seeker wins", 1, colors["text"])
                            screen.blit(
                                winner, (WIDTH - winner.get_width() - 10, 10))
                            show_maze(self.maze)
                            pygame.display.flip()
                            break
                elif last_seen != None:  # if hider is not in vicinity, seeker will trace to the last seen position
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    if prioritized != None:
                        A_star_ann = None
                        prioritized = None
                    self.seeker.reset_known_map()
                    successor = self.seeker.trace_hider(
                        self.maze, self.MAP_DIMENSIONS, last_seen)  # go to last seen position
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    if self.seeker.current_pos == last_seen:
                        last_seen = None
                elif announce_in_vicinity and (prioritized == None or prioritized == []):
                    if random_pos != None:
                        random_pos = None
                        A_star_res = None
                    self.seeker.reset_known_map()
                    for i in range(len(self.hiders)):
                        if self.announcements[i] and self.announcements[i].get_pos() == ann_pos:
                            prioritized = self.announcements[i].get_info()
                            break
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    if A_star_ann == None:
                        prioritized = None
                        self.seeker = self.seeker.clone()
                        self.seeker.reset_known_map()
                        self.seeker.format_map_by_vision(logic_vision(
                            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1]))
                        continue
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                elif A_star_ann != None:
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                    if len(A_star_ann) == 0:
                        A_star_ann = None
                elif A_star_ann == None and prioritized != None and prioritized != []:
                    furthest = self.seeker.furthest_from_self(prioritized)
                    A_star_ann = self.seeker.trace_random(
                        self.maze, self.MAP_DIMENSIONS, furthest)
                    if A_star_ann == None:
                        prioritized = None
                        self.seeker = self.seeker.clone()
                        continue
                    A_star_ann.pop(0)
                    successor = self.seeker.move_to_pos(
                        self.maze, self.MAP_DIMENSIONS, A_star_ann[0])
                    swap(self.maze, self.seeker.current_pos, A_star_ann[0])
                    self.seeker = successor
                    vision = logic_vision(
                        self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
                    self.seeker.format_map_by_vision(vision)
                    for cell in vision:
                        if cell in prioritized:
                            prioritized.remove(cell)
                    A_star_ann.pop(0)
                elif random_pos != None:
                    if A_star_res == None:
                        A_star_res = self.seeker.trace_random(
                            self.maze, self.MAP_DIMENSIONS, random_pos)
                        if A_star_res == None:
                            random_pos = None
                            continue
                        A_star_res.pop(0)
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        A_star_res.pop(0)
                    else:
                        successor = self.seeker.move_to_pos(
                            self.maze, self.MAP_DIMENSIONS, A_star_res[0])
                        swap(self.maze, self.seeker.current_pos, A_star_res[0])
                        self.seeker = successor
                        self.seeker.format_map_by_vision(logic_vision(
                            self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1]))
                        A_star_res.pop(0)
                        if len(A_star_res) == 0:
                            A_star_res = None
                            random_pos = None
                else:
                    successor = self.seeker.move(
                        self.maze, self.MAP_DIMENSIONS)
                    if type(successor) == tuple:
                        random_pos = successor
                    else:
                        self.seeker = successor
                SCORE -= 1
            else:
                turn_so_far += 1
                for i in range(len(self.hiders)):
                    move = self.hiders[i].move(
                        self.maze, self.MAP_DIMENSIONS, 3)
                    ann_prev_pos = None
                    if self.announcements[i]:
                        ann_prev_pos = self.announcements[i].get_pos()
                    if self.hiders[i].current_pos == move.current_pos:
                        announcement = self.hiders[i].announce(
                            turn_so_far, self.maze, self.MAP_DIMENSIONS)
                        if announcement:
                            self.announcements[i] = None
                            self.announcements[i] = announcement
                            ann_pos = announcement.get_pos()
                            if ann_prev_pos and self.maze[ann_prev_pos[0]][ann_prev_pos[1]] == 6:
                                self.maze[ann_prev_pos[0]][ann_prev_pos[1]] = 0
                            self.maze[ann_pos[0]][ann_pos[1]] = 6
                    else:
                        if self.announcements[i]:  
                            if self.maze[self.announcements[i].get_pos()[0]][self.announcements[i].get_pos()[1]] == 6:
                                self.maze[self.announcements[i].get_pos()[0]][self.announcements[i].get_pos()[1]] = 0
                            self.announcements[i] = None
                    self.hiders[i] = move
                    if self.maze[self.hiders[i].current_pos[0]][self.hiders[i].current_pos[1]] == 0 or self.maze[self.hiders[i].current_pos[0]][self.hiders[i].current_pos[1]] == 6:
                        self.maze[self.hiders[i].current_pos[0]][self.hiders[i].current_pos[1]] = 2
                if turn_so_far >= 6:
                    turn_so_far = 0
            screen.fill(colors["background"])
            vision = logic_vision(
                self.maze, 3, self.seeker.current_pos[0], self.seeker.current_pos[1], self.MAP_DIMENSIONS[0], self.MAP_DIMENSIONS[1])
            show_map = copy.deepcopy(self.maze)
            for cell in vision:
                if show_map[cell[0]][cell[1]] == 0:
                    show_map[cell[0]][cell[1]] = 4
            handle_event()
            turn_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Seeker's turn" if not turn else "Hider's turn", 1, colors["text"])
            screen.blit(turn_text, (10, 10))
            score_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Score: " + str(SCORE), 1, colors["text"])
            run_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Run: #" + str(RUN), 1, colors["text"])
            FPS_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "FPS: " + str(math.ceil(clock.get_fps())), 1, colors["text"])
            time = pygame.time.get_ticks() / 1000
            time_text = pygame.font.Font("Font/Dune_Rise.otf", 20).render(
                "Time: " + format_time(time), 1, colors["text"])
            screen.blit(time_text, (WIDTH - 10 - time_text.get_width(), HEIGHT - 10 - time_text.get_height()))
            screen.blit(run_text, (10, HEIGHT - 10 - run_text.get_height()))
            screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))
            screen.blit(FPS_text, (WIDTH - 10 - FPS_text.get_width(), 10))
            show_maze(show_map)
            pygame.display.flip()
            clock.tick(FPS)
            turn = not turn
        RUN += 1
            
    def run(self):
        global LEVEL, ITERATION
        pygame.display.set_caption("Hide-and-Seek")
        for i in range(ITERATION):
            handle_event()
            self.reset()
            if LEVEL == "1":
                self.level_1()
            elif LEVEL == "2":
                self.level_2(len(self.hiders))
            elif LEVEL == "3":
                self.level_3(len(self.hiders))
        pygame.time.wait(1000)
        handle_event()
        screen.fill((95,146,145))
        text = pygame.font.Font("Font/Dune_Rise.otf", 56).render(
            "Game Over", 1, (255, 255, 255))
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.flip()
        PAUSE = True
        while PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    PAUSE = False
                elif event.type == pygame.KEYDOWN:
                    PAUSE = False
        pygame.quit()
        
    def display(self):
        running = True
        pygame.display.set_caption("Maze")
        print_maze(self.maze)
        # screen.fill((95, 146, 145))
        show_maze(self.maze)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
        pygame.quit()