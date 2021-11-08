import sys
import pygame
import refait
from bases import *
from json import load as json_load

# ----- charger le fichier json contenant les infos concernant les entités ------------------
with open('Entities.json') as json_file:
    Entities = json_load(json_file)
# --------------------------------------------------
# some basic colors who could be used
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (140, 140, 137)
BLACK = (0,0,0)
# --petits parametres pour être plus lisible--
ecartement = 10 # = 10 px du bord // des autres objets // ...    ====> uniquement pour la "mise en page" (=pas obligatoire d'utiliser ce parmatres, mais peut etre utile)
bg_color = GREY # GRIS
icon_color = BLUE
mark_thickness = 7
screen_size = (940, 400)
icon_mark_color = BLACK
icon_mark_wait_color = (76, 84, 81) # kinda RED
# ---------------------------------------------

pygame.init()

# création de la fenetre avec les paramètres définis au-dessus
window = main(screen_size, ecartement, bg_color, icon_color, icon_mark_color, mark_thickness)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
    # Création des images
knight = refait.create_someone(Entities, "gentil", "Knight", "arthur", image("img/knight.png"))
knight.image.load_with_color_filter(WHITE)
knight.image.resize((50,50))
#----------------------------------------------------------     

mage = refait.create_someone(Entities, "gentil", "Mage", "Merlin l'enchanteur", image("img/mage.png"))
mage.image.load_with_color_filter(WHITE)
mage.image.resize((50,50))
#----------------------------------------------------------     

rogue = refait.create_someone(Entities, "gentil", "Rogue", "Je n'ai pas d'idée de nom", image("img/rogue.png"))
rogue.image.load_with_color_filter(WHITE)
rogue.image.resize((50,50))
#----------------------------------------------------------     

orc = refait.create_someone(Entities, "mechant", "Orc", "Azog", image("img/orc.png"))
orc.image.load_with_color_filter(WHITE)
orc.image.resize((50,50))
#----------------------------------------------------------     

ghost = refait.create_someone(Entities, "mechant", "Ghost", "Bill", image("img/ghost.png"))
ghost.image.load_with_color_filter(WHITE)
ghost.image.resize((50,50))
#----------------------------------------------------------  
cursed_knight = refait.create_someone(Entities, "mechant", "Cursed_Knight", "Lancelot du lac", image("img/cursed_knight.png"))
cursed_knight.image.load_with_color_filter((76,76,76))
cursed_knight.image.resize((50,50))
#----------------------------------------------------------     

mad_king = refait.create_someone(Entities, "hardcore", "Mad_King", "Aerys II Targaryen", image("img/mad_king.png"))
mad_king.image.load_with_color_filter(WHITE)
mad_king.image.resize((50,50))
#----------------------------------------------------------
 
goblin = refait.create_someone(Entities, "hardcore", "Goblin_Team", "Je n'ai toujours pas d'idée de nom xD", image("img/goblin.png"))
goblin.image.load_with_color_filter((58,58,58))
goblin.image.resize((50,50))
#----------------------------------------------------------     
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

#                                        Les icones (= les sélecteurs)

# 2 listes qui vont contenir chacunes des icones
icones_gentil = []
icones_mechant = []
icones_hardcore = []

    # on crée et on ajoute (avec la fonction "add_icon_to_list") 3 icones à la liste "icones_gentil" 
window.add_icon_to_list(icones_gentil, knight.image.picture, pygame.Rect(0, 0, 50, 50), BLACK, icon_mark_wait_color, knight) 
window.add_icon_to_list(icones_gentil, mage.image.picture, pygame.Rect(60, 0, 50, 50), BLACK, icon_mark_wait_color, mage)
window.add_icon_to_list(icones_gentil, rogue.image.picture, pygame.Rect(120, 0, 50, 50), BLACK, icon_mark_wait_color, rogue)
    # on crée et on ajoute (avec la fonction "add_icon_to_list") 3 icones à la liste "icones_mechant" 
window.add_icon_to_list(icones_mechant, orc.image.picture, pygame.Rect(0, 60, 50, 50), BLACK, icon_mark_wait_color, orc)
window.add_icon_to_list(icones_mechant, ghost.image.picture, pygame.Rect(60, 60, 50, 50), BLACK, icon_mark_wait_color, ghost)
window.add_icon_to_list(icones_mechant, cursed_knight.image.picture, pygame.Rect(120, 60, 50, 50), BLACK, icon_mark_wait_color, cursed_knight)
    # on crée et on ajoute (avec la fonction "add_icon_to_list") 2 icones à la liste "icones_hardcore" 
window.add_icon_to_list(icones_hardcore, mad_king.image.picture, pygame.Rect(0, 120, 50, 50), BLACK, icon_mark_wait_color, mad_king)
window.add_icon_to_list(icones_hardcore, goblin.image.picture, pygame.Rect(60, 120, 50, 50), BLACK, icon_mark_wait_color, goblin)


    # on regroupe les icônes contenues dans la liste "icones_gentil" ensemble
window.create_class_icons_from_the_icon_list(icones_gentil)
    # on fait la même chose pour la liste "icones_mechant"
window.create_class_icons_from_the_icon_list(icones_mechant)
    # on fait la même chose pour la liste "icones_hardcore"
window.create_class_icons_from_the_icon_list(icones_hardcore)

# /!\
# /!\   L'ORDRE a de l'IMPORTANCE : premier ajoutés = "au-dessus" des autres (voir plus bas les fonctions "window.icons_change_top/bottom()")
# /!\

#-------------------------------Création de carrés/buttons---------------------------------------


# Choix de la disposition et de la taille des éléments sur l'écran, de la façon la plus modulable possible (= en fonction de la taille de la fenetre)
character_rect = pygame.Rect((int(window.ECARTEMENT), int(window.ECARTEMENT)), (int(window.SCREEN_SIZE[0]/2.5), int(window.SCREEN_SIZE[1]*0.75))) # (x,y),(width, height)
ideology_rect = pygame.Rect((character_rect.x, 2*character_rect.y+character_rect.height), (character_rect.width, window.SCREEN_SIZE[1]-(3*character_rect.y+character_rect.height)))
validation_rect = pygame.Rect((800, 200), (70, 20))

# Ajout des "Rect" (=des carrés) dans la classe "main" (la 'window') pour pouvoir les afficher/ les utiliser
window.add_a_new_rect(character_rect, WHITE)
window.add_a_new_rect(ideology_rect, WHITE)

window.add_a_new_button(Button(validation_rect, [BLUE, RED, YELLOW], RED, ['first text', 'second text'], 'first text'))

while window.running:
    if window.get_button_color(validation_rect) == BLUE:
        print("BLEU est activé!!!!")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                window.icons_detect_collision(pygame.mouse.get_pos())
                window.buttons_detect_collision(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                window.icons_change_to_left()
            elif event.key == pygame.K_RIGHT:
                window.icons_change_to_right()
            elif event.key == pygame.K_UP:
                window.icons_change_top()
            elif event.key == pygame.K_DOWN:
                window.icons_change_bottom()
            elif event.key == pygame.K_RETURN:
                window.get_icon_info()

    window.blit_screen()
    window.draw_rects()
    window.draw_buttons()
    window.icons_draw()
    window.update_screen_rects()




"""
une_image = pygame.Surface((50,50))
une_image.fill(COULEUR) # création d'une image et remplissage de celle-ci
"""