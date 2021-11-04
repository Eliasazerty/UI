import sys
import pygame
import refait

pygame.init()

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

class icon: # = 1 icône qui peut être mise en relation avec d'autres grâce à la classe "icons"
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

class icons: # = 1 groupe de plusieurs icônes
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

class main: # pour pouvoir tout gérer
    def __init__(self, screen_size, ecartement, background_color, icon_color, icon_mark_color, mark_thickness):

        # constantes
        self.SCREEN_SIZE = screen_size
        self.ECARTEMENT = ecartement
        self.BACKGROUND_COLOR = background_color
        self.ICON_COLOR = icon_color
        self.ICON_MARK_COLOR = icon_mark_color
        self.MARK_THICKNESS = mark_thickness
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.running = True
        self.Rects_dic = {} # { ID : [RECT, COLOR, FILL] } || if BUTTON: { ID: [RECT, <class 'Button'>, FILL]}
        self.ID_dic = {} #    { ID : TYPE_OF_RECT}  (= BUTTON, RECT, ...)

        # some basic colors who could be used
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRIS = (140, 140, 137)
        self.BLACK = (0,0,0)

        self.all_icons = [] # list with all the icons the screen have [icons1, icons2] => is egal to : [[icon1,icon2,icon3,...], [icon1,icon2,icon3,...],...]
        self.all_rects = {} # dic with all the rect with their name: {"name" : pygame.Rect()}
    
    def add_icon_to_list(self, icon_list, img, rect, mark_color): # [+] mark_color = self.ICON_MARK_COLOR
        icon_list.append(icon(img, rect, self.screen, mark_color, self.BACKGROUND_COLOR, self.MARK_THICKNESS))
    
    def create_class_icons_from_the_icon_list(self, icon_list):
        self.all_icons.append(icons(icon_list))
    
    def add_a_new_rect(self, type_of_rect, rect_of_the_thing, color_of_the_rect):
        self.Rects_dic[self.get_highest_ID(self.ID_dic)+1] = [rect_of_the_thing, color_of_the_rect, 1]
        self.ID_dic[self.get_highest_ID(self.ID_dic)+1] = str(type_of_rect)
    
    def get_highest_ID(self, dic):
        biggest_id = -1
        for id in dic.keys():
            if id > biggest_id:
                biggest_id = id
        return biggest_id
    
    # fonctions pour pouvoir afficher les choses

    def draw_rects(self):
        for i in range(self.get_highest_ID(self.ID_dic)+1):
            if self.ID_dic[i] == "RECT":
                pygame.draw.rect(self.screen, self.Rects_dic[i][1], self.Rects_dic[i][0], self.Rects_dic[i][2])
            elif self.ID_dic[i] == "BUTTON":
                pygame.draw.rect(self.screen, self.Rects_dic[i][1].get_color(), self.Rects_dic[i][0], self.Rects_dic[i][2])

    def update_screen_rects(self):
        pygame.display.flip() 

    def blit_screen(self):  # afficher le fond d'écran
        self.screen.fill(self.BACKGROUND_COLOR)
    
    # fonctions pour faire fonctionner les icônes
    
    def icons_detect_collision(self, mouse_pos):
        for icons in self.all_icons:
            icons.detect_collision(mouse_pos)
    
    def icons_change_to_left(self):
        for icons in self.all_icons:
            icons.change_to_left()
    
    def icons_change_to_right(self):
        for icons in self.all_icons:
            icons.change_to_right()
    
    def icons_draw(self):
        for icons in self.all_icons:
            icons.draw()