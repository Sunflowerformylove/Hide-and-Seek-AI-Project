import pygame
from Seeker import *
from Support import *

WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 50
MAP_DIMENSIONS = (8, 11)
PAUSE = False

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def read_maze(filename: str) -> list[list[int]]:
    maze = []
    file = open(filename, "r")
    for line in file:
        temp = []
        for char in line:
            if char != "\n" and char != " ":
                temp.append(int(char))
        maze.append(temp)
    return maze

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
    border = 3
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, "black", (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 2:
                pygame.draw.rect(screen, "red", (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 3:
                pygame.draw.rect(screen, (0, 0, 34), (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 4:
                pygame.draw.rect(screen, "teal", (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, "black", (offset_width + j * CELL_SIZE, offset_height + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), border)

maze = read_maze("maze.txt")
seeker = Seeker(maze, 3, 0, None)
(move_result, hider_pos)= seeker.move(MAP_DIMENSIONS)
path1 = backtrace(move_result)
trace = seeker.trace_hider(MAP_DIMENSIONS, hider_pos, move_result)
path2 = backtrace(trace)
screen.fill("white")
pygame.display.flip()
for node in path2:
    pause_frame()
    pygame.display.flip()
    show_maze(node)
    pygame.display.flip()
    clock.tick(1)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

pygame.quit()