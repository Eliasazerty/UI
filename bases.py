import sys
import pygame
import refait

BACKGROUND_COLOR = (0,0,0) # = black

pygame.init()

# les classes

class Button:
    def __init__(self, rect, colors, active_color, text_list, active_text):
        self.rect = rect
        self.colors = colors # = list of colors
        self.active_color = active_color
        self.text_list = text_list
        self.active_text = active_text

    def change_color(self):
        self.colors.append(self.colors[0])
        self.colors.pop(0)
        self.active_color = self.colors[0]

    def change_text(self):
        self.text_list.append(self.text_list[0])
        self.text_list.pop(0)
        self.active_text = self.text_list[0]

    def get_color(self):
        return self.active_color
    
    def get_text(self):
        return self.active_text
    
    def is_colliding(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def detect_collision(self, position):
        if self.is_colliding(position):
            self.change_color()
            self.change_text()

class icon:
    def __init__(self, img, rect, screen):
        self.img = img
        self.img.fill((255, 255, 0))
        self.rect = rect
        self.mark_rect_blit = False
        self.mark_color = (140, 140, 137) # = Gris
        self.screen = screen

    def is_colliding(self, position):
        if self.rect.collidepoint(position):
            return True
        return False
    
    def detect_collision(self, position):
        if self.is_colliding(position):
            self.react_to_collision()
    
    def react_to_collision(self):
        if not self.mark_rect_blit: # si le "surlignage" n'est pas activé
                self.mark_rect(self.mark_color)
                self.mark_rect_blit = True
        else:
            self.mark_rect((0,0,0))
            self.mark_rect_blit = False
        
    def mark_rect(self, color):
        pygame.draw.rect(self.screen, color, self.rect, 7)
    
    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class icons: # [+] faire la sélection au clavier
    def __init__(self, icon_list):
        if len(icon_list) > 0:
            self.number_of_icons = len(icon_list)
            self.icon_list = icon_list
            self.activated_icon_index = 0
            self.old_icon_index = len(icon_list)-1 # pour initialiser, on définit le dernier icône comme étant le dernier selectionné (mais inutile)
        else:
            sys.exit("icon_list vide !")
        
        self.mark_selected_icon() # pour avoir une icône selectionnée de base
    
    def draw(self):
        for icon in self.icon_list:
            icon.draw()
    
    def detect_collision(self, mouse_pos):
        for index_icon, icon in enumerate(self.icon_list):
            if icon.is_colliding(mouse_pos):
                self.actualize_old_icon()
                self.activated_icon_index = index_icon
                self.mark_selected_icon()
    
    def mark_selected_icon(self):
        self.icon_list[self.activated_icon_index].mark_rect((140, 140, 137)) # GRIS
        self.icon_list[self.old_icon_index].mark_rect((0,0,0))
    
    def change_to_right(self):
        self.actualize_old_icon()
        if self.activated_icon_index < self.number_of_icons-1:
            self.activated_icon_index += 1
        else:
            self.activated_icon_index = 0 # si on ne peut pas "aller" plus à droite, on retourne au début
        self.mark_selected_icon()
    
    def change_to_left(self):
        self.actualize_old_icon()
        if self.activated_icon_index > 0:
            self.activated_icon_index -= 1
        else:
            self.activated_icon_index = self.number_of_icons-1 # si on ne peut pas "aller" plus à gauche, on retourne à la fin
        self.mark_selected_icon()

    def actualize_old_icon(self):
        self.old_icon_index = self.activated_icon_index #on enregistre l'ancienne position pour pouvoir appliquer un cache dessus

# les paramètres généraux ( = constantes)

SCREEN_SIZE = (740, 400)  # width, height = x, y
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRIS = (140, 140, 137)
Rects_dic = {} # { ID : [RECT, COLOR, FILL] } || if BUTTON: { ID: [RECT, <class 'Button'>, FILL]}
ID_dic = {} #    { ID : TYPE_OF_RECT}  (= BUTTON, RECT, ...)
ECARTEMENT = 10 # 10 px du bord // des autres objets // ...

screen = pygame.display.set_mode(SCREEN_SIZE)
running = True

# Choix de la disposition et de la taille des éléments sur l'écran, de la façon la plus modulable possible (= en fonction de la taille de la fenetre)
character_rect = pygame.Rect((int(ECARTEMENT), int(ECARTEMENT)), (int(SCREEN_SIZE[0]/2.5), int(SCREEN_SIZE[1]*0.75))) # (x,y),(width, height)
ideology_rect = pygame.Rect((character_rect.x, 2*character_rect.y+character_rect.height), (character_rect.width, SCREEN_SIZE[1]-(3*character_rect.y+character_rect.height)))
#valid_rect = pygame.Rect(()) # choisir l'emplacement !!!!!!!!!

ent_img = pygame.Surface((50,50))
ent_img.fill(BLUE)
ent_butt0 = icon(ent_img, pygame.Rect(0,0, 50, 50), screen)

ent_butt1 = icon(ent_img, pygame.Rect(60,0, 50, 50), screen)

ent_butt2 = icon(ent_img, pygame.Rect(120,0, 50, 50), screen)

real_icons = icons([ent_butt0, ent_butt1, ent_butt2])

# fonctions pour pouvoir afficher les choses

def draw_rects(screen, ID_dic, highest_ID):
    for i in range(highest_ID+1):
        if ID_dic[i] == "RECT":
            pygame.draw.rect(screen, Rects_dic[i][1], Rects_dic[i][0], Rects_dic[i][2])
        elif ID_dic[i] == "BUTTON":
            pygame.draw.rect(screen, Rects_dic[i][1].get_color(), Rects_dic[i][0], Rects_dic[i][2])

def update_screen_rects(screen):
    pygame.display.flip() 

def get_highest_ID(ID_dic):
    biggest_id = -1
    for id in ID_dic.keys():
        if id > biggest_id:
            biggest_id = id
    return biggest_id



Rects_dic[get_highest_ID(ID_dic)+1] = [character_rect, WHITE, 1]
ID_dic[get_highest_ID(ID_dic)+1] = "RECT"

Rects_dic[get_highest_ID(ID_dic)+1] = [ideology_rect, WHITE, 1]
ID_dic[get_highest_ID(ID_dic)+1] = "RECT"

# déclaration des éléments qui seront utilisés 

"""
Valid_button =    Button(Valid_button_box, [GREEN, RED], GREEN, ["Valider", "Sur ?"], "Valider")
Ideology_button = Button(Ideology_button_box, [GREEN, RED, YELLOW], RED, ["GENTIL", "Mechant", "Compliqué"], "Gentil")
icon_entity = entity_icon(icon_entity_img, icon_entity_box, screen)



Rects_dic[get_highest_ID(ID_dic)+1] = [Character_box, WHITE, 1]
ID_dic[get_highest_ID(ID_dic)+1] = "RECT"
Rects_dic[get_highest_ID(ID_dic)+1] = [Valid_button_box, Valid_button, 0]
ID_dic[get_highest_ID(ID_dic)+1] = "BUTTON"
Rects_dic[get_highest_ID(ID_dic)+1] = [Ideology_button_box, Ideology_button, 0]
ID_dic[get_highest_ID(ID_dic)+1] = "BUTTON"
"""