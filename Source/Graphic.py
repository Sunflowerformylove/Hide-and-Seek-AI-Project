import pygame
from Seeker import *
from copy import deepcopy

WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 20
PAUSE = False

# Initialize pygame and screen
# pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def read_maze(filename: str) -> list[list[int]]:
    maze = []
    file = open(filename, "r")
    line = file.readline().split()
    map_dimensions = [int(line[0]), int(line[1])]
    for line in file:
        temp = []
        for char in line:
            if char != "\n" and char != " ":
                temp.append(int(char))
        maze.append(temp)
    return (maze, map_dimensions)

def handle_event() -> None:
    global PAUSE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
                while PAUSE:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                PAUSE = not PAUSE
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                quit()

def show_maze(maze: list[list[int]]) -> None:
    offset_width = WIDTH // 2 - len(maze[0]) * CELL_SIZE // 2
    offset_height = HEIGHT // 2 - len(maze) * CELL_SIZE // 2
    border = 1
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, (2, 1, 10), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 2:
                pygame.draw.rect(screen, (115, 29, 216), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 3:
                pygame.draw.rect(screen, (72, 169, 166), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 4:
                pygame.draw.rect(screen, (213, 176, 172), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (2, 1, 10), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), border)


def level_1(maze: list[list[int,int]], map_dimensions: tuple[int, int]):
    seeker = Seeker(maze, 3, 0, None)
    (current, hider) = seeker.move(map_dimensions)
    result = current.trace_hider(map_dimensions, hider, current)
    return backtrace(result)

def level_2(maze: list[list[int,int]], map_dimensions: tuple[int, int], num_hiders: int):
    seeker = Seeker(maze, 3, 0, None)
    while num_hiders > 0:
        (current, hider) = seeker.move(map_dimensions)
        seeker = current.trace_hiders(map_dimensions, hider, current, len(hider))
        num_hiders -= 1
    return backtrace(seeker)

def level_3(maze: list[list[int,int]], map_dimensions: tuple[int, int], num_hiders: int):
    result = zero_sum(maze, map_dimensions, num_hiders)
    return result

# maze, MAP_DIMENSIONS = read_maze("Tests/maze.txt")
# temp_maze = deepcopy(maze)
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((255, 255, 255))
#     show_maze(maze)
#     pygame.display.flip()
#     # seeker = Seeker(maze, 3, 0, None) 
#     # path = level_2(maze, MAP_DIMENSIONS,4)
#     # step = 0
#     # font = pygame.font.Font(None, 36)
#     # for node in path:
#     #     handle_event()
#     #     screen.fill((255, 255, 255))
#     #     show_maze(node)
#     #     turn = node[1]
#     #     turn_text = font.render(f"Turn: {turn}", True, (0, 0, 0))
#     #     turnRect = turn_text.get_rect()
#     #     turnRect.topright = (WIDTH - 10, 10)
#     #     screen.blit(turn_text, turnRect)
#     #     text = font.render(f"Step: {step}", True, (0, 0, 0))
#     #     textRect = text.get_rect()
#     #     textRect.topleft = (10, 10)
#     #     screen.blit(text, textRect)
#     #     pygame.display.flip()
#     #     clock.tick(5)
#     #     step += 1
#     # maze = deepcopy(temp_maze)
#     # pygame.time.wait(3000)
# pygame.quit()