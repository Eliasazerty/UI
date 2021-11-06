# Créé par yvelt, le 16/10/2021 en Python 3.7
# Refait par eliasazerty, le 25/10/2021 en Python 3.8.5
import sys
import json

with open('Entities.json') as json_file:
    Entities = json.load(json_file)
#Entities = { # name, damage, hp, defense, speed, precision
#
#    "Knight" : ['', 55, 1500, 25, 5, 5],      # Gentil
#    "Mage"   : ['', 60, 1000, 10, 5, 15],
#    "Rogue"  : ['', 40, 800, 5, 37, 37],
#    "Orc"    : ['Orc', 70, 5, 1250, 2, 2],      #méchant
#    "Water_elemental" : ['Water_elemental', 50, 10, 1000, 15, 10],
#    "Ghost" :           ['Ghost', 40, 0, 600, 40, 25],
#    "Cursed_Knight" :   ['Cursed_Knight', 40, 20, 2000, 10, 25],
#    "Deviant_Alexa" :   ['Deviant_Alexa', 55, 10, 900, 15, 35],
#    "Goblin_Team" : ['Goblin_Team', 45, 5, 1000, 7, 7],     #compliqué
#    "Mad_King" :    ['Mad_King', 30, 35, 2300, 5, 10],
#    "Prankster_Gh": ['Prankster_Gh', 40, 0, 400, 80, 50],
#    "Chad"  :       ['Chad', 60, 20, 1200, 0, 0],
#    "SCM"   :       ['S.C.M.', 45, 10, 1600, 10, 10]
#}

class Entity:
    def __init__(self, characteristics, ideology, entity_type, image = False): # characteristics = [name, damage, hp, defense, speed, precision]
        self.name = characteristics[0]
        self.damage = characteristics[1]
        self.defense = characteristics[2]
        self.hp = characteristics[3]
        self.speed = characteristics[4]
        self.precision = characteristics[5]

        self.entity_type = entity_type
        if image != False: # = si cet argument existe 
            self.image = image
        else:
            self.image = None

        if ideology == "gentil":
            self.ideology = "a great"
        else:
            self.ideology = "an evil"

    def presentation(self):
        print(f"Caracteristics of {self.name}, {self.ideology} {self.entity_type}:")
        print(f"\t\tATK [{self.damage}] \n \t\tHP [{self.hp}] \n \t\tdefense [{self.defense}] \n \t\tspeed [{self.speed}] \n \t\tprecision [{self.precision}]")

def create_someone(Entities_dic, ideology, type_of_entity, entity_name, image):
    try:
        entite = Entities_dic[type_of_entity]
        entite[0] = entity_name
        Someone = Entity(entite, ideology, type_of_entity, image)
    except:
        print(f"ERROR: No entity of type {type_of_entity} found !")
        sys.exit()
    return Someone