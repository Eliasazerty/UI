import sys
import pygame
import refait
from bases import *

pygame.init()

# Choix de la disposition et de la taille des éléments sur l'écran, de la façon la plus modulable possible (= en fonction de la taille de la fenetre)
character_rect = pygame.Rect((int(ECARTEMENT), int(ECARTEMENT)), (int(SCREEN_SIZE[0]/2.5), int(SCREEN_SIZE[1]*0.75))) # (x,y),(width, height)
ideology_rect = pygame.Rect((character_rect.x, 2*character_rect.y+character_rect.height), (character_rect.width, SCREEN_SIZE[1]-(3*character_rect.y+character_rect.height)))
# Les icones (= les sélecteurs)
ent_img = pygame.Surface((50,50))
ent_img.fill(ICON_COLOR)
ent_butt0 = icon(ent_img, pygame.Rect(0,0, 50, 50), screen, GRIS, BACKGROUND_COLOR, MARK_THICKNESS)
ent_butt1 = icon(ent_img, pygame.Rect(60,0, 50, 50), screen, GRIS, BACKGROUND_COLOR, MARK_THICKNESS)
ent_butt2 = icon(ent_img, pygame.Rect(120,0, 50, 50), screen, GRIS, BACKGROUND_COLOR, MARK_THICKNESS)
real_icons = icons([ent_butt0, ent_butt1, ent_butt2])

# Ajout des "Rect" dans des listes pour pouvoir les afficher
Rects_dic[get_highest_ID(ID_dic)+1] = [character_rect, WHITE, 1]
ID_dic[get_highest_ID(ID_dic)+1] = "RECT"

Rects_dic[get_highest_ID(ID_dic)+1] = [ideology_rect, WHITE, 1]
ID_dic[get_highest_ID(ID_dic)+1] = "RECT"

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