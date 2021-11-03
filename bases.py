import sys
import pygame
import refait

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
    def __init__(self, img, rect, screen, mark_color, background_color, mark_thickness):
        self.img = img
        self.rect = rect
        self.mark_color = mark_color #(140, 140, 137) # = Gris
        self.background_color = background_color
        self.screen = screen
        self.mark_thickness = mark_thickness

    def is_colliding(self, position):
        if self.rect.collidepoint(position):
            return True
        return False
    
    def detect_collision(self, position):
        if self.is_colliding(position):
            self.react_to_collision()
    
    def react_to_collision(self):
        self.mark_rect(self.mark_color)

    def mark_rect(self, color):
        pygame.draw.rect(self.screen, color, self.rect, self.mark_thickness)
    
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
        self.icon_list[self.activated_icon_index].mark_rect(self.icon_list[self.activated_icon_index].mark_color) # GRIS
        self.icon_list[self.old_icon_index].mark_rect(self.icon_list[self.activated_icon_index].background_color) # BLACK
    
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
BLACK = (0,0,0)
Rects_dic = {} # { ID : [RECT, COLOR, FILL] } || if BUTTON: { ID: [RECT, <class 'Button'>, FILL]}
ID_dic = {} #    { ID : TYPE_OF_RECT}  (= BUTTON, RECT, ...)
ECARTEMENT = 10 # 10 px du bord // des autres objets // ...
BACKGROUND_COLOR = BLACK
ICON_COLOR = BLUE
MARK_THICKNESS = 7

screen = pygame.display.set_mode(SCREEN_SIZE)
running = True

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