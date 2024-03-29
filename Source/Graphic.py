import pygame
from Seeker import *
from copy import deepcopy
from Global import *

exec()
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
    offset_width = WIDTH // 2 - len(maze[0]) * CELL_SIZE // 2
    offset_height = HEIGHT // 2 - len(maze) * CELL_SIZE // 2
    border = 1
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:   # Ivory
                pygame.draw.rect(screen, (242, 245, 234), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 2: # Persian green
                pygame.draw.rect(screen, (51, 153, 137), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 3: # Imperial red
                pygame.draw.rect(screen, (229, 56, 59), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 4: # Coral
                pygame.draw.rect(screen, (247, 135, 100), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 6: # Ash grey
                pygame.draw.rect(screen, (157, 180, 171), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else: # White-ish 
                pygame.draw.rect(screen, (253, 254, 250), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), border)