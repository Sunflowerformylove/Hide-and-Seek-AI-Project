import pygame
from Seeker import *
from Global import *
from Args import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
    global CELL_SIZE
    global WIDTH, HEIGHT
    global MODE, DARK_MODE, LIGHT_MODE, DUNE_MODE
    colors = {}
    if MODE == "DARK":
        colors = DARK_MODE
    elif MODE == "LIGHT":
        colors = LIGHT_MODE
    elif MODE == "DUNE":
        colors = DUNE_MODE
    else:
        colors = DARK_MODE
    CELL_SIZE = min((HEIGHT - 50) // len(maze), (WIDTH - 50) // len(maze[0]))
    offset_width = WIDTH // 2 - len(maze[0]) * CELL_SIZE // 2
    offset_height = HEIGHT // 2 - len(maze) * CELL_SIZE // 2
    border = 1
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, colors["wall"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 2:
                pygame.draw.rect(screen, colors["hider"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 3:
                pygame.draw.rect(screen, colors["seeker"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 4:
                pygame.draw.rect(screen, colors["observed"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 6:
                pygame.draw.rect(screen, colors["announcement"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 7:
                pygame.draw.rect(screen, colors["object"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, colors["free"], (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), border)