from MyEnums import * # NOQA
from settings import * # NOQA
import math
import random



class Player: #class with some hard-coded heuristics, neural player will have the same options but actually choose
    
    def __init__(self, name):
                
        self.name = name
        self.pos = 0
        self.money = STARTING_MONEY
        self.in_jail = False
        self.turns_in_jail = 0
        self.jail_card = 0
        self.doubles = 0
        self.properties = [] #there will be two records of owning properties, one in the board and one from the player 
        self.retired = False
        self.place = 0
    
    
    def buy_decision(self, price):
        if self.money > price:
            return buy_decision.BUY
        
        return buy_decision.AUCTION
    
    
    def jail_decision(self):
        
        return jail_decision.ROLL
    
    
    def mortgage_decision(self, index):
        
        if self.money < 0:
            return decision.YES
        
        else:
            return decision.NO
        
    
    def accept_trade(self):
        
        return decision.NO
    
    
    def offer_trade(self):
        
        return decision.NO
    
    def decide_sell_house(self, index):
        
        if self.money < 0:
            return 15
        
        else:
            return 0
        
    def decide_build_house(self, index):
        return 1

    def decide_bid(self, price):

        return price
    
    def decide_unmortgage(self, price):
        
        if price < self.money:
            return decision.YES
        
        return decision.NO





        