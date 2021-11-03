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
BACKGROUND_COLOR = GREEN
ICON_COLOR = BLUE
MARK_THICKNESS = 7
running = True # pour la boucle de la fenetre
