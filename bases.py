import sys
import pygame
import refait

pygame.init()

class image: # = permet de charger/redimensionner et ajouter de la transparence à une image
    def __init__(self, path):
        self.path = path
        self.picture = None
        
    def load(self):
        self.picture = pygame.image.load(self.path).convert()
    
    def load_with_transparence(self):
        self.picture = pygame.image.load(self.path).convert_alpha()

    def load_with_color_filter(self, color):
        self.picture = pygame.image.load(self.path)
        self.picture.set_colorkey(color)
        self.picture.convert_alpha()
    
    def resize(self, size):
        self.picture = pygame.transform.scale(self.picture, size)
    
    def infos(self):
        print("Img:")
        print(f"\tWIDTH = {self.picture.get_width()}")
        print(f"\tHEIGHT = {self.picture.get_height()}")

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
            return True
        return False

class icon: # = 1 icône qui peut être mise en relation avec d'autres grâce à la classe "icons"
    def __init__(self, img, rect, screen, mark_color, mark_thickness, mark_wait_color, Entity):
        self.img = img
        self.rect = rect
        self.mark_color = mark_color #(140, 140, 137) # = Gris
        self.screen = screen
        self.mark_thickness = mark_thickness
        self.mark_wait_color = mark_wait_color

        if Entity != False: # = they're an Entity linked to this icon
            self.entity = Entity
        else:
            self.entity = None

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
    
    def draw(self, selected_icon_should_being_draw):
        for icon in self.icon_list:
            icon.draw()
        if selected_icon_should_being_draw:
            self.mark_selected_icon()
        else:
            self.mark_selected_wait_icon()
    
    def detect_collision(self, mouse_pos):
        for index_icon, icon in enumerate(self.icon_list):
            if icon.is_colliding(mouse_pos):
                self.activated_icon_index = index_icon
                return True
        return False
    
    def mark_selected_icon(self):
        self.icon_list[self.activated_icon_index].mark_rect(self.icon_list[self.activated_icon_index].mark_color) # GRIS

    def mark_selected_wait_icon(self): # pour la classe "main" ==> permet de "switcher" entre différents groupe d' icones en affichant une nouvelle couleur
        self.icon_list[self.activated_icon_index].mark_rect(self.icon_list[self.activated_icon_index].mark_wait_color)

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
    def __init__(self, screen, icon_mark_color, mark_thickness, bg_img):

        # constantes
        self.SCREEN_SIZE = screen.get_size()
        self.ICON_MARK_COLOR = icon_mark_color
        self.MARK_THICKNESS = mark_thickness
        self.BG_IMG = bg_img
        self.screen = screen
        # variables utiles dans tout le programme
        self.running = True
        self.rects_list = []  # [RECT, COLOR, FILL]
        self.button_list = [] # [<class 'Button'>, FILL]

        self.all_icons = [] # list with all the icons the screen have [icons1, icons2] => is egal to : [[icon1,icon2,icon3,...], [icon1,icon2,icon3,...],...]
        self.all_rects = {} # dic with all the rect with their name: {"name" : pygame.Rect()}

        self.index_of_actual_icons_used = 0 # pour pouvoir savoir quelles icones changer lors d'évenements du clavier
    
 #                                                   [+] default: mark_color = self.ICON_MARK_COLOR
    def add_icon_to_list(self, icon_list, img, rect, mark_color, mark_wait_color, Entity = False): 
        icon_list.append(icon(img, rect, self.screen, mark_color, self.MARK_THICKNESS, mark_wait_color, Entity))

    def create_class_icons_from_the_icon_list(self, icon_list):
        self.all_icons.append(icons(icon_list))
    
    def add_a_new_rect(self, rect_of_the_thing, color_of_the_rect, fill=1): # fill -> 1 = just the borders / 0 = totaly filled
        self.rects_list.append([rect_of_the_thing, color_of_the_rect, fill])
    
    def add_a_new_button(self, Button_class, fill = 0): # fill -> 1 = just the borders / 0 = totaly filled
        self.button_list.append([Button_class, fill])
        
    # fonctions pour pouvoir afficher les choses à l'écran

    def draw_rects(self):
        for rect in self.rects_list: # on parcourt tout les éléments de la liste et on les affiche
            pygame.draw.rect(self.screen, rect[1], rect[0], rect[2])

    def draw_buttons(self): # on parcourt tout les éléments de la liste et on les affiche
        for button in self.button_list:
            pygame.draw.rect(self.screen, button[0].get_color(), button[0].rect, button[1])
                
    def update_screen_rects(self):
        pygame.display.flip() 

    def blit_screen(self):  # afficher le fond d'écran
        self.screen.blit(self.BG_IMG.picture, (0,0))
    
    # fonction pour pouvoir détecter la sélection d'un bouton:
    def buttons_detect_collision(self, mouse_pos):
        for button_characteristics in self.button_list:
            if button_characteristics[0].detect_collision(mouse_pos): # si un bouton est "touché"
                return                             # on quitte la fonction (la souris est à un seul endroit à la fois) = optimisation

    def get_button_color(self, rect):
        for button_characteristics in self.button_list:
            if button_characteristics[0].rect == rect:
                return button_characteristics[0].get_color()
    
    def get_button_list(self):
        return self.button_list
    # fonction pour afficher les infos de l'icone en sélection

    def get_icon_info(self):
        print("ICON:")
        current_icons = self.all_icons[self.index_of_actual_icons_used]
        activated_icon_index = current_icons.activated_icon_index
        if current_icons.icon_list[activated_icon_index].entity != None:
            print("\t", end="")
            current_icons.icon_list[activated_icon_index].entity.presentation()
        print(f"\tWIDTH: {current_icons.icon_list[activated_icon_index].rect.width}")
        print(f"\tHEIGHT: {current_icons.icon_list[activated_icon_index].rect.height}")


    # fonctions pour faire fonctionner les icônes
    
    def icons_detect_collision(self, mouse_pos):
        for index, icons in enumerate(self.all_icons): # truc avec enumerate() pour pouvoir changer self.index_of_actual_icon_used
            if icons.detect_collision(mouse_pos):
                self.index_of_actual_icons_used = index
                return
    
    def icons_change_to_left(self):
        self.all_icons[self.index_of_actual_icons_used].change_to_left()
    
    def icons_change_to_right(self):
        self.all_icons[self.index_of_actual_icons_used].change_to_right()
    
    def icons_change_bottom(self):
        if self.index_of_actual_icons_used < len(self.all_icons)-1:
            self.index_of_actual_icons_used += 1
    
    def icons_change_top(self):
        if self.index_of_actual_icons_used > 0:
            self.index_of_actual_icons_used -= 1


    def icons_draw(self):
        for index, icons in enumerate(self.all_icons): # selected_icon_should_being_draw
            if index == self.index_of_actual_icons_used:
                icons.draw(selected_icon_should_being_draw=True)
            else:
                icons.draw(selected_icon_should_being_draw=False)