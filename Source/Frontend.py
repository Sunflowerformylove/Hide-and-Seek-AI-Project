import pygame
from Global import *
from Graphic import *

pygame.init()
running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while running:
    screen.fill((0,0,0))
    welcome = pygame.font.Font(None, 54).render("Hide and Seek", 1, (255, 255, 255))
    screen.blit(welcome, (WIDTH // 2 - welcome.get_width() // 2, 20))
    slogan = pygame.font.Font(None, 20).render("Slightly better than guessing, Slightly worse than AI", 1, (255, 255, 255))
    screen.blit(slogan, (WIDTH // 2 - slogan.get_width() // 2, 80))
    pygame.display.flip()
    handle_event()
    
pygame.quit()