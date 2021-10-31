import sys
import pygame
import refait
from bases import *

pygame.init()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #   /!\ pygame.KEYDOWN
            if event.button == 1:
                real_icons.detect_collision(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                real_icons.change_to_left()
            elif event.key == pygame.K_RIGHT:
                real_icons.change_to_right()
    

    draw_rects(screen, ID_dic, get_highest_ID(ID_dic))
    real_icons.draw()
    update_screen_rects(screen)