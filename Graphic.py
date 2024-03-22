import pygame
from Seeker import *

WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 50
PAUSE = False

# Initialize pygame and screen
pygame.init()
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

def toggle_pause() -> None:
    global PAUSE
    PAUSE = not PAUSE
    
def pause_frame() -> None:
    global PAUSE
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()
                while PAUSE:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                toggle_pause()
                    if not PAUSE:
                        break

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

maze, MAP_DIMENSIONS = read_maze("maze1.txt")

# print_maze(maze)
# print(MAP_DIMENSIONS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    seeker = Seeker(maze, 3, 0, None)
    hiders = 2
    path = None
    while hiders > 0:
        path = seeker.move(MAP_DIMENSIONS)
        path = seeker.trace_hider(MAP_DIMENSIONS, path[1], path[0], len(path[1]))
        maze = path.map
        path = backtrace(path)
        hiders -= 1
    # move_result = seeker.move(MAP_DIMENSIONS)
    # move_result = seeker.trace_hider(MAP_DIMENSIONS, move_result[1], move_result[0], len(move_result[1]))
    # path = backtrace(move_result)
    for node in path:
        screen.fill((255, 255, 255))
        show_maze(node)
        pygame.display.flip()
        pause_frame()
        clock.tick(10)

pygame.quit()