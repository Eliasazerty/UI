import sys
import pygame
import refait
from parametres import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

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
        if background_color == mark_color:
            print("WARNING: background color is the same as the mark color !")
        self.screen = screen
        self.mark_thickness = mark_thickness

    def is_colliding(self, position):
        if self.rect.collidepoint(position):
            return True
        return False
    
    def mark_rect(self, color):
        pygame.draw.rect(self.screen, color, self.rect, self.mark_thickness)
    
    def draw(self):
        self.screen.blit(self.img, (self.rect.x, self.rect.y))

class icons: # [+] faire la sélection au clavier
    def __init__(self, icon_list):
        if len(icon_list) > 0:
            self.number_of_icons = len(icon_list)
            self.icon_list = icon_list
            self.activated_icon_index = 0
        else:
            sys.exit("icon_list vide !")
        
        self.mark_selected_icon() # pour avoir une icône selectionnée de base
    
    def draw(self):
        for icon in self.icon_list:
            icon.draw()
        self.mark_selected_icon()
    
    def detect_collision(self, mouse_pos):
        for index_icon, icon in enumerate(self.icon_list):
            if icon.is_colliding(mouse_pos):
                self.activated_icon_index = index_icon
    
    def mark_selected_icon(self):
        self.icon_list[self.activated_icon_index].mark_rect(self.icon_list[self.activated_icon_index].mark_color) # GRIS

    def change_to_right(self):
        if self.activated_icon_index < self.number_of_icons-1:
            self.activated_icon_index += 1
        else:
            self.activated_icon_index = 0 # si on ne peut pas "aller" plus à droite, on retourne au début
    
    def change_to_left(self):
        if self.activated_icon_index > 0:
            self.activated_icon_index -= 1
        else:
            self.activated_icon_index = self.number_of_icons-1 # si on ne peut pas "aller" plus à gauche, on retourne à la fin

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

def blit_screen(screen, background_color):
    screen.fill(background_color)

def add_a_new_rect(type_of_rect, rect_of_the_thing, color_of_the_rect, Rects_dic, ID_dic, highest_ID_of_IDdic):
    Rects_dic[highest_ID_of_IDdic+1] = [rect_of_the_thing, color_of_the_rect, 1]
    ID_dic[highest_ID_of_IDdic+1] = str(type_of_rect)