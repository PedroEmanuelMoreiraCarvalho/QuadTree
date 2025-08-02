import pygame
import time
from QuadTree import QuadTree

screen_width = 900
screen_height = 600

pygame.init()
window = pygame.display.set_mode((screen_width,screen_height))
font = pygame.font.SysFont('Tohama',40, True,False)
pygame.display.update()

running = True
pause = False
delta_time = 0.1

quad_tree = QuadTree(0,0,screen_width,screen_height)

while running:
    pygame.draw.rect(window, (0,0,0), pygame.Rect(0,0,screen_width,screen_height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            quad_tree.addPoint(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            quad_tree.removePoint(pygame.mouse.get_pos())

    #update
    if not pause:
        quad_tree.update()

    # render
    quad_tree.render(window)

    pygame.display.update()
    time.sleep(delta_time)