import sys
import pygame
import refait
from bases import *

# --petits parametres pour être plus lisible--
ecartement = 10 # 10 px du bord // des autres objets // ...
bg_color = (140, 140, 137) # GRIS
icon_color = (0, 0, 255) #BLUE
mark_thickness = 7
screen_size = (740, 400)
icon_mark_color = (0,0,0) # BLACK
# ---------------------------------------------

pygame.init()
window = main(screen_size, ecartement, bg_color, icon_color, icon_mark_color, mark_thickness) # création de la fenetre


# création des images qui vont être utilisée :
img_gentil = pygame.Surface((50,50))
img_gentil.fill(window.ICON_COLOR) # création de l'image des icones et remplissage

mechant_img = pygame.Surface((50,50))
mechant_img.fill(window.YELLOW) # création de l'image des icones et remplissage

# Les icones (= les sélecteurs)
icones_gentil = []
icones_mechant = []
    # on crée et on ajoute (avec la fonction "add_icon_to_list") 3 icones à la liste "icones_gentil" 
window.add_icon_to_list(icones_gentil, img_gentil, pygame.Rect(0, 0, 50, 50), window.BLACK) 
window.add_icon_to_list(icones_gentil, img_gentil, pygame.Rect(60, 0, 50, 50), window.BLACK)
window.add_icon_to_list(icones_gentil, img_gentil, pygame.Rect(120, 0, 50, 50), window.BLACK)
    # on crée et on ajoute (avec la fonction "add_icon_to_list") 3 icones à la liste "icones_mechant" 
window.add_icon_to_list(icones_mechant, mechant_img, pygame.Rect(0, 60, 50, 50), window.BLACK)
window.add_icon_to_list(icones_mechant, mechant_img, pygame.Rect(60, 60, 50, 50), window.BLACK)
window.add_icon_to_list(icones_mechant, mechant_img, pygame.Rect(120, 60, 50, 50), window.BLACK)

    # on regroupe les icônes contenues dans la liste "icones_gentil"
window.create_class_icons_from_the_icon_list(icones_gentil)
window.create_class_icons_from_the_icon_list(icones_mechant) # on fait pareil pour la liste "icones_mechant"

# Choix de la disposition et de la taille des éléments sur l'écran, de la façon la plus modulable possible (= en fonction de la taille de la fenetre)
character_rect = pygame.Rect((int(window.ECARTEMENT), int(window.ECARTEMENT)), (int(window.SCREEN_SIZE[0]/2.5), int(window.SCREEN_SIZE[1]*0.75))) # (x,y),(width, height)
ideology_rect = pygame.Rect((character_rect.x, 2*character_rect.y+character_rect.height), (character_rect.width, window.SCREEN_SIZE[1]-(3*character_rect.y+character_rect.height)))

# Ajout des "Rect" dans la classe "main" pour pouvoir les afficher/ les utiliser
window.add_a_new_rect("RECT", character_rect, window.WHITE)
window.add_a_new_rect("RECT", ideology_rect, window.WHITE)

while window.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #   /!\ pygame.KEYDOWN
            if event.button == 1:
                window.icons_detect_collision(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                window.icons_change_to_left()
            elif event.key == pygame.K_RIGHT:
                window.icons_change_to_right()
    
    window.blit_screen()
    window.draw_rects()
    window.icons_draw()
    window.update_screen_rects()