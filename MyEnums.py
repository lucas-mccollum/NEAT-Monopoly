from enum import Enum


class decision(Enum):
    
    YES = 0
    NO = 1
    

class buy_decision(Enum):
    
    BUY = 0
    AUCTION = 1

class jail_decision(Enum):
    
    ROLL = 0
    PAY = 1
    CARD = 2
    
class Tile(Enum):
    
    OTHER = 0 #this is Go and Visiting Jail
    PROPERTY = 1
    CHEST = 2
    CHANCE = 3
    TRAIN = 4
    UTILITY = 5
    TAX = 6
    JAIL = 7
    
    
class Cards(Enum):
    
    ADVANCE = 0
    GOJ = 1
    JAIL = 2
    FINE = 3
    UTILITY = 4
    RAIL = 5
    GENERAL_REPAIRS = 6 #these two are the same, but one goes in community and one goes in chance
    STREET_REPAIRS = 7
    REWARD = 8
    CHAIRMAN = 9
    BACK = 10
    BIRTHDAY = 11
    
class card_entry:
    
        def __init__(self, card, value):
            
            self.card = card
            self.value = value
    


    
    
    
    
    
    
    
    