from MyEnums import *
from settings import *
from Player import Player
from NetInputs import NetInputs 
import random
import numpy as np
import math
import os
import neat

import time 

time1 = time.time()

"""
Big change here...

"""


class NetworkPlayer:
    
    def __init__(self, genome):
        
        self.genome = genome #this will be a genome defined by neat-python
        
        #aside from the genome, everything else should be the same...
        
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
        
        output = self.genome.activate(network.inputs)
        
        if output[0] > 0.5:
            return buy_decision.BUY
        
        return buy_decision.AUCTION
    
    def jail_decision(self):
        
        output = self.genome.activate(network.inputs)
        
        if output[1] < 0.333:
            
            return jail_decision.ROLL
        
        elif output[1] < 0.666:
            
            return jail_decision.CARD
        
        return jail_decision.PAY
    
    def mortgage_decision(self, index):
        
        output = self.genome.activate(network.inputs)
        
        if output[2] > 0.5:
            
            return decision.YES
        
        return decision.NO
    
    def accept_trade(self):
        
        output = self.genome.activate(network.inputs)
        
        if output[3] > 0.5:
            
            return decision.YES
        
        return decision.NO
    
    def offer_trade(self):
        
        output = self.genome.activate(network.inputs)
        
        if output[4] > 0.5:
            
            return decision.YES
        
        return decision.NO
    
    def decide_sell_house(self, index):
        
        output = self.genome.activate(network.inputs)
        houses = 15 * output[5]
        
        return int(houses)
    
    def decide_build_house(self, index):
        
        output = self.genome.activate(network.inputs)
        houses = output[6] * 15
        
        return int(houses)
    
    def decide_bid(self, index):
        
        output = self.genome.activate(network.inputs)
        offer = 5000 * output[7]
        
        return offer
    
    def decide_unmortgage(self, index):
        
        output = self.genome.activate(network.inputs)
        
        if output[8] > 0.5:
            
            return decision.YES
        
        return decision.NO
        






#---------------Board constants---------------#

PLAYER_COUNT = 4

BANK_INDEX = -1
GO_BONUS = 200

BOARD_LENGTH = 40
STALEMATE = 500


JAIL_INDEX = 10
JAIL_PENALTY = 50

MORTGAGE_INTEREST = 0.1




#---------------Define all possible penalties---------------#

PROPERTY_PENALTIES =[[2, 10, 30, 90, 160, 250 ],
    [ 4, 20, 60, 180, 320, 450 ],
    [ 6, 30, 90, 270, 400, 550 ],
    [ 8, 40, 100, 300, 450, 600 ],
    [ 10, 50, 150, 450, 625, 750 ],
    [ 12, 60, 180, 500, 700, 900 ],
    [ 14, 70, 200, 550, 750, 950 ],
    [ 16, 80, 220, 600, 800, 1000 ],
    [ 18, 90, 250, 700, 875, 1050 ],
    [ 20, 100, 300, 750, 925, 1100 ],
    [ 22, 110, 330, 800, 975, 1150 ],
    [ 22, 120, 360, 850, 1025, 1200 ],
    [ 26, 130, 390, 900, 1100, 1275 ],
    [ 28, 150, 450, 1000, 1200, 1400 ],
    [ 35, 175, 500, 1100, 1300, 1500 ],
    [ 50, 200, 600, 1400, 1700, 2000 ]]

UTILITY_POSITIONS = [12, 28]
UTILITY_PENALTIES = [4, 10]

TRAIN_POSITIONS = [5, 15, 25, 35]
TRAIN_PENALTIES = [25, 50, 100, 200]





#---------------Cost of buying and building on properties and completing sets of colours---------------#

COSTS = [0, 60, 0, 60, 200, 200, 100, 0, 100, 120, 
         0, 140, 150, 140, 160, 200, 180, 0, 180, 200, 
         0, 220, 0, 220, 240, 200, 260, 260, 150, 280, 
         0, 300, 300, 0, 320, 200, 0, 250, 100, 400]

TILES = [Tile.OTHER, Tile.PROPERTY, Tile.CHEST, Tile.PROPERTY, Tile.TAX, Tile.TRAIN, Tile.PROPERTY, Tile.CHANCE, Tile.PROPERTY, Tile.PROPERTY, 
         Tile.OTHER, Tile.PROPERTY, Tile.UTILITY, Tile.PROPERTY, Tile.PROPERTY, Tile.TRAIN, Tile.PROPERTY, Tile.CHEST, Tile.PROPERTY, Tile.PROPERTY, 
         Tile.OTHER, Tile.PROPERTY, Tile.CHANCE, Tile.PROPERTY, Tile.PROPERTY, Tile.TRAIN, Tile.PROPERTY, Tile.PROPERTY, Tile.UTILITY, Tile.PROPERTY, 
         Tile.JAIL, Tile.PROPERTY, Tile.PROPERTY, Tile.CHEST, Tile.PROPERTY, Tile.TRAIN, Tile.CHANCE, Tile.PROPERTY, Tile.TAX, Tile.PROPERTY]



HOUSE_PRICE = [50, 50, 50, 50, 
               100, 100, 100, 100, 
               150, 150, 150, 150, 
               200, 200, 200, 200] #each property has an index from 0-15, which is why there are only 16 entries, not 40

SET =  [[1, 3, -1],
        [6, 8, 9],
        [11, 13, 14],
        [16, 18, 19],
        [21, 23, 24],
        [26, 27, 29],
        [31, 32, 34],
        [37, 39, -1]] #-1 are the colours with only two properties






#---------------Information about the state of each tile on the board---------------#

MORTGAGED = [False] * 40
OWNER = [-1] * 40
HOUSES = [0] * 40
ORIGINAL = [-1] * 40 #this shows who has the property, probably for trading purposes
PROPERTY_ID = [-1, 0, -1, 1, -1, -1, 2, -1, 2, 3,
               -1, 4, -1, 4,  5, -1, 6, -1, 6, 7, 
               -1, 8, -1, 8,  9, -1,10, 10,-1,11,
               -1, 12,12,-1, 13,-1, -1, 14,-1,15] #gives the property ID, those with the same attributes have the same ID

FITNESS = [0, 0, 0, 0]





#---------------create class for adding cards to the community and chance decks---------------#

class card_entry:

    def __init__(self, card, value):
        
        self.card = card
        self.value = value


#---------------setting up the initial states of the game---------------#
        
current_turn = 0
count = 0
last_roll = 0

chance = []
chest = []

network = NetInputs() #initialise the network inputs

players = []

remaining = PLAYER_COUNT


"""
New bits here trying to connect NetworkPlayer, so getting rid of this bit for the time being


for i in range(PLAYER_COUNT):
    players.append(Player(f"Player {i}"))
    network.set_position(i, players[i].pos)
    network.set_money(i, players[i].money)
    
    
"""    

#---------------NEW BIT WITH NETWORKS AND GENOMES---------------#



"""


#I think this is where the board should have its run method?
#Then we can just put the genomes in here and run the rest as usual

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-monopoly')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

p = neat.Population(config)

for genome_id, genome in p.population.items():
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    players.append(NetworkPlayer(net))
    network.set_position(genome_id - 1, players[genome_id - 1].pos) #when doing this later, I think we'll have to do ((genome_id -1) % 4)
    network.set_money(genome_id - 1, players[genome_id - 1].money)



NEW NOTE - this is being added to the end of the program to see if we can run the whole thing at once


"""


chance = []
chest = []



chance.append(card_entry("ADVANCE", 0))
chance.append(card_entry("ADVANCE", 5))
chance.append(card_entry("ADVANCE", 11))
chance.append(card_entry("ADVANCE", 24))
chance.append(card_entry("ADVANCE", 39))
chance.append(card_entry("RAIL", 0))
chance.append(card_entry("RAIL", 0))
chance.append(card_entry("UTILITY", 0))
chance.append(card_entry("REWARD", 50))
chance.append(card_entry("GENERAL_REPAIRS", 0))
chance.append(card_entry("GOJ", 0))
chance.append(card_entry("FINE", 15))
chance.append(card_entry("BACK", 3))
chance.append(card_entry("CHAIRMAN", 0))
chance.append(card_entry("REWARD", 150))
chance.append(card_entry("JAIL", 0))


chance = random.sample(chance, len(chance))


chest.append(card_entry("REWARD", 10))
chest.append(card_entry("REWARD", 50))
chest.append(card_entry("REWARD", 100))
chest.append(card_entry("REWARD", 100))
chest.append(card_entry("REWARD", 100))
chest.append(card_entry("REWARD", 200))
chest.append(card_entry("FINE", 25))
chest.append(card_entry("FINE", 50))
chest.append(card_entry("FINE", 100))
chest.append(card_entry("FINE", 100))
chest.append(card_entry("ADVANCE", 0))
chest.append(card_entry("GOJ", 0))
chest.append(card_entry("BIRTHDAY", 0))
chest.append(card_entry("STREET_REPAIRS", 100))

chest = random.sample(chest, len(chest))



#---------------Now we can start the game mechanics!---------------#    


def roll():
    return [np.random.randint(1,6+1) for _ in range(2)] #return two random numbers between 1 and 6

def ongoing():
    
    global current_turn
    
    count = 0
    for i in range(PLAYER_COUNT):
        if not players[i].retired:
            count += 1
    
    if count > 1: 
        return -1
    elif count == 1:
        return current_turn
    



def find_sets(current_turn):
    
    
    sets = []
    props = properties(current_turn)
    
    for i in range(0, 8): #loop through all of the sets
        
        if i == 0 or i == 7: #if it's a two property set
            if SET[i][0] in props and SET[i][1] in props: #if both properties are owned by the player
                sets.append(i)
        
        else:
            if SET[i][0] in props and SET[i][1] in props and SET[i][2] in props:
                sets.append(i)
    return sets


def properties(current_turn):
    
    global OWNER
    
    prop = []
    
    for i in range(len(OWNER)):
        if OWNER[i] == current_turn:
            prop.append(i)
    
    return prop


def sell_houses(set_id, number):
    
    global HOUSES
    global SET
    global current_turn
    
    last_property = 2
    
    if set_id == 0 or set_id == 7:
        last_property = 1

    for i in range(number):
        
        smallest_no_houses = 0
        
        for j in range(last_property + 1):
            
            #want to only sell from the property with the mosts houses, so check for that
            if (HOUSES[SET[set_id][smallest_no_houses]] < HOUSES[SET[set_id][j]]):
                
                smallest_no_houses = j
            
        
        HOUSES[SET[set_id][smallest_no_houses]] -= 1
        network.set_houses(SET[set_id][smallest_no_houses], HOUSES[SET[set_id][smallest_no_houses]])

    
    
def buy_houses(set_id, number):
    
    global HOUSES
    global SET
    
    last_property = 2
    
    if set_id == 0 or set_id == 7: 
        
        last_property = 1
        
    for i in range(number):
        smallest_no_houses = last_property
        
        for j in range(last_property, -1, -1): 
            
            #now we want to build on the property with the fewest houses, so slightly different from the sell_houses method
            if (HOUSES[SET[set_id][smallest_no_houses]] > HOUSES[SET[set_id][j]]):
                
                smallest_no_houses = j
            
        HOUSES[SET[set_id][smallest_no_houses]] += 1
        network.set_houses(SET[set_id][smallest_no_houses], HOUSES[SET[set_id][smallest_no_houses]])
 
           
def payment(player1, fine, player2 = None):
    #we're combining the two payment methods, so the default is just that there is no other player.
    
    global remaining #don't really know if this will work but we'll see
    
    if fine:
        players[player1].money -= fine
        network.set_money(player1, players[player1].money)
        if player2:
            players[player2].money += fine
            network.set_money(player2, players[player2].money)
    
    if players[player1].money < 0:
        #same logic as 'before turn', start with selling houses
        sets = find_sets(player1)
        sets_length  = len(sets)
        
        for i in range(sets_length):
            
            total_houses = HOUSES[SET[sets[i]][0]] + HOUSES[SET[sets[i]][1]] #add the first two of the set
            
            if sets[i] != 0 and sets[i] != 7: #if the set has 3 properties, add the third property
                
                total_houses += HOUSES[SET[sets[i]][2]]
                
            max_to_sell = total_houses
            
            network.set_turn(player1)
            network.set_choice(SET[sets[i]][0])
            
            decision = players[player1].decide_sell_house(sets[i]) # this method actually returns the number of houses to sell
            
            network.clear_choices()
                        
            houses_to_sell = min(max_to_sell, decision)
            
            if houses_to_sell > 0:
                
                players[player1].money +=  0.5 * houses_to_sell * HOUSE_PRICE[PROPERTY_ID[SET[sets[i]][0]]] #sell the house for half value
                sell_houses(sets[i], houses_to_sell)
                network.set_money(player1, players[player1].money)
                
        
    #then prompt to mortgage
    
    players[player1].properties = properties(player1)
    
    item_count = len(players[player1].properties)
    for i in range(item_count):
        
        item = players[player1].properties[i]
        
        network.set_turn(player1)
        network.set_choice(players[player1].properties[i])
        
        decision = players[current_turn].mortgage_decision(item).name
        
        network.clear_choices()
        
        if decision == "YES":
            MORTGAGED[item] = True
            players[current_turn].money += COSTS[item] / 2
            network.set_mortgaged(item, 1)
    
    #if still no money, player is bankrupt. Two different methods for payment or payment to player, just split with if statement
    
    if players[player1].money < 0:
        
        if player2:
            
            players[player2].money += players[player1].money #player 2 can't be given more money than player 1 has so has to give back deficit
            
            players[player1].properties = properties(player1)

            item_count = len(players[player1].properties)
            price_of_houses = 0
            
            for i in range(item_count):
                
                prop = players[player1].properties[i]
                OWNER[prop] = player2
                
                players[player2].properties = properties(player2)
                
                network.set_owner(prop, player2)
                
                if HOUSES[prop] > 0:
                    
                    number_to_sell = HOUSES[prop]
                    value = (number_to_sell * HOUSE_PRICE[PROPERTY_ID[prop]])
                    price_of_houses += value
                    HOUSES[prop] = 0
            
            players[player2].money += price_of_houses
            players[player1].properties.clear()
            players[player1].retired = True
                        
            network.set_money(player2, players[player2].money)
            
            players[player1].place = remaining
            
            remaining -= 1
            
            print(f"Player {player1} finishes in {players[player1].place}")
            

            
        
        else:
            
            players[player1].properties = properties(player1)
            
            item_count = len(players[player1].properties)
            for i in range(item_count):
                prop = players[player1].properties[i]
                OWNER[prop] = BANK_INDEX
                HOUSES[prop] = 0
                network.set_owner(prop, -1)
            
                
            players[player1].properties.clear()
            players[player1].retired = True
            
            players[player1].place = remaining
            
            remaining -= 1
            print(f"Player {player1} finishes in {players[player1].place}")



def advance_to_train():
    
    global current_turn
    
    if players[current_turn].retired:
        return
    
    pos = players[current_turn].pos
    
    for i in range(4):
        if pos < TRAIN_POSITIONS[i]:
            players[current_turn].pos = TRAIN_POSITIONS[i]
            network.set_position(current_turn, TRAIN_POSITIONS[i])
            break
    
    players[current_turn].money += GO_BONUS
    players[current_turn].pos = TRAIN_POSITIONS[0]
    
    network.set_money(current_turn, players[current_turn].money)
    network.set_position(current_turn, TRAIN_POSITIONS[0])

def advance_to_utility():
    
    global current_turn

    pos = players[current_turn].pos
    
    if pos < UTILITY_POSITIONS[0]:
        players[current_turn].pos = UTILITY_POSITIONS[0]
        network.set_position(current_turn, UTILITY_POSITIONS[0])
    
    elif pos < UTILITY_POSITIONS[1]: 
        players[current_turn].pos = UTILITY_POSITIONS[1]
        network.set_position(current_turn, UTILITY_POSITIONS[1])
    
    else: 
        players[current_turn].money += GO_BONUS
        players[current_turn].pos = UTILITY_POSITIONS[0]
        network.set_position(current_turn, UTILITY_POSITIONS[0])
        network.set_money(current_turn, players[current_turn].money)




def count_trains(owner):
    
    players[owner].properties = properties(owner)
    
    no_items = len(players[owner].properties)
    count = 0
    
    for i in range(no_items):
        if players[owner].properties[i] in TRAIN_POSITIONS:
            count += 1
    
    return count

def count_utilities(owner):
    
    players[owner].properties = properties(owner)
    
    no_items = len(players[owner].properties)
    count = 0
    for i in range(no_items):
        if players[owner].properties[i] in UTILITY_POSITIONS:
            count += 1
    
    return count

def pick_chance_card():
    
    global current_turn
  
    players[current_turn].properties = properties(current_turn)
    
    card = chance.pop(0)
    chance.append(card)
    if card.card == Cards.ADVANCE.name:
        if players[current_turn].pos > card.value:
            players[current_turn].money += GO_BONUS
            network.set_money(current_turn, players[current_turn].money)
                    
        players[current_turn].pos = card.value       
        network.set_position(current_turn, players[current_turn].pos)
        
        land_on_tile()
    
    elif card.card == Cards.REWARD.name:
        players[current_turn].money += card.value
        network.set_money(current_turn, players[current_turn].money)
    
    elif card.card == Cards.FINE.name:
        payment(current_turn, card.value) 
    
    elif card.card == Cards.BACK.name:
        players[current_turn].pos -= card.value
        network.set_position(current_turn, players[current_turn].pos)
        
        land_on_tile()
    
    elif card.card == Cards.GOJ.name:
        players[current_turn].jail_card = 1 
        network.set_cards(current_turn, 1)
    
    elif card.card == Cards.JAIL.name:
        players[current_turn].pos = JAIL_INDEX
        players[current_turn].doubles = 0
        players[current_turn].in_jail = True
        
        network.set_jail(current_turn, 1)
        network.set_position(current_turn, players[current_turn].pos)
    
    elif card.card == Cards.RAIL.name:
        advance_to_train()
        land_on_tile()
    
    elif card.card == Cards.UTILITY.name:
        advance_to_utility()
        land_on_tile()
    
    elif card.card == Cards.CHAIRMAN.name:
        for i in range(PLAYER_COUNT):
            if i == current_turn:
                continue
            if not players[i].retired:
                payment(current_turn, 50, i)
    
    elif card.card == Cards.GENERAL_REPAIRS.name:
        
        houses = 0
        hotels = 0
        item_count = len(players[current_turn].properties)
        
        for i in range(item_count):
            prop = players[current_turn].properties[i]
            
            if HOUSES[prop] <= 4:
                houses += HOUSES[prop]
            else:
                hotels += 1
        
        payment(current_turn, houses * 25 + hotels * 100)


def pick_chest_card():
    
    global current_turn

    card = chest.pop(0)
    chest.append(card)
    
    if card.card == Cards.ADVANCE.name:
        if players[current_turn].pos > card.value:
            players[current_turn].money += GO_BONUS
            network.set_money(current_turn, players[current_turn].money)
        
        players[current_turn].pos = card.value
        network.set_position(current_turn, players[current_turn].pos)
        
        land_on_tile()
        
        
    elif card.card == Cards.REWARD.name:
        players[current_turn].money += card.value
        network.set_money(current_turn, players[current_turn].money)
        
    elif card.card == Cards.FINE.name:
        payment(current_turn, card.value)
    
    elif card.card == Cards.GOJ.name:
        players[current_turn].jail_card = 1
        network.set_cards(current_turn, 1)
    
    elif card.card == Cards.JAIL.name:
        players[current_turn].pos = JAIL_INDEX
        players[current_turn].in_jail = True
        players[current_turn].doubles = 0
        
        network.set_jail(current_turn, 1)
        network.set_position(current_turn, players[current_turn].pos)
    
    elif card.card == Cards.BIRTHDAY.name:
        
        for i in range(PLAYER_COUNT):
            if i == current_turn:
                continue
            if not players[i].retired:
                payment(i, 10, current_turn)
        
    elif card.card == Cards.STREET_REPAIRS.name:
        
        houses = 0
        hotels = 0
        item_count = len(players[current_turn].properties)
        
        for i in range(item_count):
            prop = players[current_turn].properties[i]
            
            if HOUSES[prop] <= 4:
                houses += HOUSES[prop]
            else:
                hotels += 1
        
        payment(current_turn, houses * 40 + hotels * 115)
        


def fitness_for_draw():
    #basically sell all player's assets, then rank players based on total assets
    total_assets = [0, 0, 0, 0]
    for i in range(PLAYER_COUNT):
        assets = 0
        props = properties(i)
        for prop in props:
            assets += COSTS[prop]
        
        assets += players[i].money
        total_assets[i] = assets
    
    fitness = [sorted(total_assets).index(x) for x in total_assets]
    
    return fitness



def trading():
    
    global current_turn

    """
    The basic principal here is that we define a list of possible traders that a player can trade with. Then, we allow a given number of 
    trade attempts (which can be fine-tuned at a later date) and essentially just randomise the proposed trades between the two players.
    
    """
    
    players[current_turn].properties = properties(current_turn)
    
    #first, make dictionary of potential traders
    candidate_traders = {}
    
    for i in range(PLAYER_COUNT):
        if i == current_turn:
            continue
        if players[i].retired:
            continue
        
        candidate_traders[i] = players[i]
        
    #if no traders, return
    if not candidate_traders:
        return
    
    #set a number of maximum parameters, just makes life simpler
    MAX_ATTEMPTS = 4
    MAX_ITEMS = 5
    MAX_MONEY = 500
    
    for i in range(MAX_ATTEMPTS):
        #firstly we initiate a random number of items to give and to whom to give them
        player_items = len(players[current_turn].properties)
        items_to_trade = random.randint(0, min(MAX_ITEMS, player_items))            
        trader_id, trader = random.choice(list(candidate_traders.items())) #as candidate_traders is a dict, this is how we access the info
        
        trader.properties = properties(trader_id)
        
        trader_items = len(trader.properties)
        items_to_receive = random.randint(0, min(MAX_ITEMS, trader_items))
        
        if players[current_turn].money < 0 or trader.money < 0: #players can't trade, skip to next loop iteration
            continue
        
        if items_to_trade == 0 or items_to_receive == 0: #if a player offers nothing in the trade, skip to next loop iteration
            continue
        
        #now we initiate a random amount of money for each player to trade
        
        money_to_give = random.randint(0, min(int(players[current_turn].money), MAX_MONEY))
        money_to_receive = random.randint(0, min(int(trader.money), MAX_MONEY))
        difference = money_to_give - money_to_receive
        
        #initialise and populate the lists to trade
        trade_offer = []
        possible_trade_items = players[current_turn].properties
        
        for i in range(items_to_trade): #items to trade is the number of items randomly selected to trade
            
            index = random.randint(0, len(possible_trade_items) - 1)
            trade_offer.append(possible_trade_items[index])
            possible_trade_items.pop(index)
        
        
        #initialise and populate the lists to receive
        
        return_offer = []
        possible_return_items = trader.properties
        
        for i in range(items_to_receive):
            
            index = random.randint(0, len(possible_return_items) - 1)
            return_offer.append(possible_return_items[index])
            possible_return_items.pop(index)
        
        
        
        for i in range(len(trade_offer)):
            network.set_choice(trade_offer[i])
        
        for i in range(len(return_offer)):
            network.set_choice(return_offer[i])
        
        network.set_context(difference)
        
        
        """YOU NEED TO SET CONTEXT FOR THE NETWORK HERE, THIS WILL BECOME MORE OBVIOUS WHEN YOU START IMPLEMENTING THE NETWORKS
        BUT THEY NEED TO ASSESS EACH OF THE ITEMS IN TEMS OF THEIR CONTEXT.
        
        HIS VERSION USES THE NEURAL PLAYER FOR THE WHOLE BOARD
        
        ALso interesting, he reloads the network adapter after every call to a method, presumably so the network always has the most up to date 
        information for any given decision
        """
        
        decision = players[current_turn].offer_trade().name
        
        if decision == "NO":
            
            network.clear_choices()
            continue
        
        decision2 = trader.accept_trade().name
        
        if decision2 == "NO":
            continue
        
        for i in range(len(trade_offer)):
            
            OWNER[trade_offer[i]] = trader_id
            
            players[current_turn].properties = properties(current_turn)
            trader.properties = properties(trader_id)
            
            network.set_owner(trade_offer[i], trader_id)
        
        for i in range(len(return_offer)):
         
            OWNER[return_offer[i]] = current_turn
            
            players[current_turn].properties = properties(current_turn)
            trader.properties = properties(trader_id)
            
            network.set_owner(return_offer[i], current_turn)
        
        #here you clear the whole trade selection
        network.clear_choices()
        payment(current_turn, difference, trader_id)
    
    
def auction(property_id):
    
    global current_turn
    
    
    """Not going to be multiple rounds of bidding, each player gets only one bid and the highest bid wins.
    If nobody bids above 0, then the property goes back to the bank
    
    """
    
    participation = [False] * PLAYER_COUNT
    for i in range(PLAYER_COUNT):
        if not players[i].retired:
            participation[i] = True
        
    bids = [0] * PLAYER_COUNT
    
    for i in range(PLAYER_COUNT):
        
        network.set_turn(i)
        network.set_choice(property_id)
        
        bids[i] = players[i].decide_bid(COSTS[property_id])
        
        network.clear_choices()
        
        if bids[i] > players[i].money:
            participation[i] = False
            bids[i] = 0
    
    maximum_bid = 0
    
    for i in range(PLAYER_COUNT):
        if participation[i]:
            if bids[i] > maximum_bid:
                maximum_bid = bids[i]
        
    #I think here we just make a list of all the people who've bid the max and a list of everyone else
    
    top_bidders = []
    
    for i in range(PLAYER_COUNT):
        if bids[i] == maximum_bid and maximum_bid != 0:
            top_bidders.append(i)
    
    if len(top_bidders) >= 1:
        if len(top_bidders) == 1:
            payment(top_bidders[0], maximum_bid) 
            OWNER[property_id] = top_bidders[0]
            players[top_bidders[0]].properties = properties(top_bidders[0])
            if ORIGINAL[property_id] == -1:
                ORIGINAL[property_id] = top_bidders[0]
            
            network.set_owner(property_id, top_bidders[0])
        
        else: #multiple top bidders, give it to a random one
            winner = random.choice(top_bidders)
            payment(winner, maximum_bid) 
            OWNER[property_id] = winner
            players[winner].properties = properties(winner)
            if ORIGINAL[property_id] == -1:
                ORIGINAL[property_id] = winner
            
            network.set_owner(property_id, winner)
    
    else:
        return #i.e. do nothing, nothing happens to the property
            
            
            
            
def land_on_tile():
    
    global current_turn
    global last_roll
    
    if players[current_turn].retired:
        return
    
    pos = players[current_turn].pos
    tile = TILES[pos]
    
    if tile.name == "PROPERTY":
        property_owner = OWNER[pos]
        
        if property_owner == BANK_INDEX:
            
            network.set_turn(current_turn)
            network.set_choice(pos)
            
            decision = players[current_turn].buy_decision(COSTS[pos])
            
            network.clear_choices()
            
            if decision.name == "BUY":
                if players[current_turn].money < COSTS[pos]:
                    auction(pos)
                
                else:
                    payment(current_turn, COSTS[pos]) 
                    OWNER[pos] = current_turn
                    
                    if ORIGINAL[pos] == -1:
                        ORIGINAL[pos] = current_turn
                    
                    players[current_turn].properties = properties(current_turn)
                    network.set_owner(pos, current_turn)
            
            elif decision.name == "AUCTION":
                auction(pos)
        
        elif property_owner == current_turn:
            return
        
        elif not MORTGAGED[pos]:
            #NEED TO DEFINE PAYMENT TO PLAYER, NEEDS TO INCLUDE STUFF ABOUT IF A PLAYER DEFAULTS
                            
            payment(current_turn, PROPERTY_PENALTIES[PROPERTY_ID[pos]][HOUSES[pos]], property_owner)
                
    elif tile.name == "TRAIN":
        
        train_owner = OWNER[pos]
        if train_owner == BANK_INDEX:
            
            network.set_turn(current_turn)
            network.set_choice(pos)
            
            decision = players[current_turn].buy_decision(COSTS[pos])
            
            network.clear_choices()
            
            if decision.name == "BUY":
                if players[current_turn].money < COSTS[pos]:
                    auction(pos)
                   
                else:
                    payment(current_turn, COSTS[pos])
                    OWNER[pos] = current_turn
                    
                    if ORIGINAL[pos] == -1:
                        ORIGINAL[pos] = current_turn
                    
                    players[current_turn].properties = properties(current_turn)
                    network.set_owner(pos, current_turn)
                    
            elif decision.name == "AUCTION":
            
                auction(pos)
            
        elif train_owner == current_turn:
            pass
        

            
        elif not MORTGAGED[pos]:
            
            no_trains = count_trains(train_owner)
            fine  = TRAIN_PENALTIES[no_trains - 1]
            payment(current_turn, fine, train_owner)

    elif tile.name == "UTILITY":
        
        utility_owner = OWNER[pos]
        if utility_owner == BANK_INDEX:
            
            network.set_turn(current_turn)
            network.set_choice(pos)
            
            decision = players[current_turn].buy_decision(COSTS[pos])
            
            network.clear_choices()
            
            if decision.name == "BUY":
                if players[current_turn].money < COSTS[pos]:
                    auction(pos)
                   
                else:
                    payment(current_turn, COSTS[pos]) 
                    OWNER[pos] = current_turn
                    
                    if ORIGINAL[pos] == -1:
                        ORIGINAL[pos] = current_turn
                    
                    players[current_turn].properties = properties(current_turn)
                    network.set_owner(pos, current_turn)
                    
            elif decision.name == "AUCTION":
            
                auction(pos)
            
        elif utility_owner == current_turn:
            pass
        
            
        elif not MORTGAGED[pos]:
            
            no_utilities = count_utilities(utility_owner)
            fine  = TRAIN_PENALTIES[no_utilities - 1] * last_roll
            payment(current_turn, fine, utility_owner)
    
    elif tile.name == "TAX":
        payment(current_turn, COSTS[pos])
        
        
    elif tile.name == "CHANCE":
        pick_chance_card()
        
    elif tile.name == "CHEST":
        pick_chest_card()
    
    elif tile.name == "JAIL":
        players[current_turn].in_jail = True
        players[current_turn].pos = JAIL_INDEX
        players[current_turn].doubles = 0
        
        network.set_jail(current_turn, 1)
    

def move(dice_sum):   

    global current_turn
        
    players[current_turn].pos += dice_sum
    
    if players[current_turn].pos >= BOARD_LENGTH:
        players[current_turn].money += GO_BONUS
        players[current_turn].pos -= BOARD_LENGTH
    
    network.set_money(current_turn, players[current_turn].money)
    network.set_position(current_turn, players[current_turn].pos)
    
    land_on_tile()
        
     
        
def pre_turn():
    
    global current_turn

    if players[current_turn].retired:
        return
    
    players[current_turn].properties = properties(current_turn)
    
    item_count = len(players[current_turn].properties) 
    #AH! The 'advance' bit that he talks about is because you MUST unmortgage properties (plus interest) when you have enough money
    for i in range(item_count):
        index = players[current_turn].properties[i]
        
        if MORTGAGED[index]:                
            unmortgage_price = COSTS[index] * (1 + MORTGAGE_INTEREST)
            if unmortgage_price > players[current_turn].money: #if you don't have enough money to buy it back, do nothing
                continue
            
            network.set_turn(current_turn)
            network.set_choice(index)
            
            decision = players[current_turn].decide_unmortgage(COSTS[index]).name
            
            network.clear_choices()
            
            if decision == "YES":
            
                payment(current_turn, unmortgage_price) 
                MORTGAGED[index] = False
                network.set_mortgaged(index, 0)
        
        else:
            
            network.set_turn(current_turn)
            network.set_choice(index)
            
            decision = players[current_turn].mortgage_decision(index).name
            
            network.clear_choices()
            
            if decision == "YES":
                MORTGAGED[index] = True
                players[current_turn].money += COSTS[index] / 2
                network.set_mortgaged(index, 1)
    
    sets = find_sets(current_turn)
    sets_length  = len(sets)
    
    
    for i in range(sets_length):
        
        total_houses = HOUSES[SET[sets[i]][0]] + HOUSES[SET[sets[i]][1]] #add the first two of the set
        
        if sets[i] != 0 and sets[i] != 7: #if the set has 3 properties, add the third property
            
            total_houses += HOUSES[SET[sets[i]][2]]
            
        max_to_sell = total_houses
        
        network.set_turn(current_turn)       
        
        network.set_choice(SET[sets[i]][0])
        
        decision = players[current_turn].decide_sell_house(sets[i]) # this method actually returns the number of houses to sell
        
        network.clear_choices()
        
        decision = min(max_to_sell, decision)
                
        if decision > 0:
            sell_houses(sets[i], decision)
            players[current_turn].money +=  0.5 * decision * HOUSE_PRICE[PROPERTY_ID[SET[sets[i]][0]]] #sell the house for half value

            
    
    #we pretty much just repeat this process, but this time for buying houses 
    
    sets = find_sets(current_turn)
    set_length = len(sets)
    
    for i in range(set_length):
        max_no_houses = 10
        total_houses = HOUSES[SET[sets[i]][0]] + HOUSES[SET[sets[i]][1]]
        if sets[i] != 0 and sets[i] != 7:
            max_no_houses = 15
            total_houses += HOUSES[SET[sets[i]][2]]
        
        build_max = max_no_houses - total_houses #you can only build 5 houses on each property 
        
        if build_max < 0:
            build_max = 0
        
        funds_for_building = math.floor(players[current_turn].money / HOUSE_PRICE[PROPERTY_ID[SET[sets[i]][0]]])
        
        if funds_for_building < 0:
            funds_for_building = 0
        
        build_max = min(funds_for_building, build_max)
        
        network.set_turn(current_turn)
        network.set_choice(SET[sets[i]][0])
        
        decision = players[current_turn].decide_build_house(sets[i])
        
        network.clear_choices()
        
        decision = min(decision, build_max)
        
        
        if decision > 0:
            buy_houses(sets[i], decision)
            payment(current_turn, decision * HOUSE_PRICE[PROPERTY_ID[SET[sets[i]][0]]]) 
    
    #finally we implement the trading method
    trading()
    

def increment():

    global current_turn
    current_turn += 1
    if current_turn >= PLAYER_COUNT:
        current_turn = 0
        
    
    
    

def turn():
    
    global current_turn
    global last_roll
   
    pre_turn()

    players[current_turn].properties = properties(current_turn)
    
    dice = roll() #roll dice       
    double = dice[0] == dice[1] #check if double
    double_in_jail = False
    
    last_roll = sum(dice)
    
    network.set_turn(current_turn)
    
    #first we check if the player is in jail
    if players[current_turn].in_jail:
        
        network.set_turn(current_turn)
        
        decision = players[current_turn].jail_decision().name
        
        if decision == "ROLL":
            if double:
                #reset the jail attributes to not in jail and no turns in jail
                players[current_turn].in_jail = False
                players[current_turn].turns_in_jail = 0
                
                network.set_jail(current_turn, 0)
                
                double_in_jail = True #will be used when deciding if the player gets another turn
            
            else:
                players[current_turn].turns_in_jail += 1
                if players[current_turn].turns_in_jail >= 3:
                    
                    
                    #in future this can be refactored into a function
                    payment(current_turn, JAIL_PENALTY)
                    players[current_turn].in_jail = False
                    players[current_turn].turns_in_jail = 0
                    
                    network.set_jail(current_turn, 0)
                
        
        elif decision == "PAY":
            payment(current_turn, JAIL_PENALTY)
            
            players[current_turn].in_jail = False
            players[current_turn].turns_in_jail = 0
            
            network.set_jail(current_turn, 0)
            
        
        elif decision == "CARD":
            
            if players[current_turn].jail_card > 0:
                players[current_turn].jail_card = 0
                players[current_turn].in_jail = False
                players[current_turn].turns_in_jail = 0
                
                network.set_jail(current_turn, 0)
                network.set_cards(current_turn, 0)
                
            
            else:
                #regular jail turn, again this should be refactored later
                if double:
                #reset the jail attributes to not in jail and no turns in jail
                    players[current_turn].in_jail = False
                    players[current_turn].turns_in_jail = 0
                    
                    double_in_jail = True #will be used when deciding if the player gets another turn
                    
                    network.set_jail(current_turn, 0)
            
                else:
                    players[current_turn].turns_in_jail += 1
                    if players[current_turn].turns_in_jail >= 3:
                        
                        
                        #in future this can be refactored into a function
                        payment(current_turn, JAIL_PENALTY) 
                        players[current_turn].in_jail = False
                        players[current_turn].turns_in_jail = 0
                        
                        network.set_jail(current_turn, 0)
                    
                    
    
    if not players[current_turn].in_jail:
        if not double or players[current_turn].doubles <= 1:
            
            move(sum(dice)) #move the player
    
    
    #if the player is still active, rolled a double and that double wasn't in jail
    if not players[current_turn].retired and double and not double_in_jail: 
        players[current_turn].doubles += 1
        
        if players[current_turn].doubles >= 3:
            players[current_turn].in_jail = True
            players[current_turn].doubles = 0
            players[current_turn].pos = JAIL_INDEX
            
            network.set_jail(current_turn, 1)
            
    
    outcome = end_turn((not double or players[current_turn].retired or players[current_turn].in_jail))
    
    return outcome
    

def end_turn(outcome):
    global remaining
    global current_turn
    global count
    global FITNESS
    
    if outcome:
        increment()
        count2 = 0
        while players[current_turn].retired and count2 <= PLAYER_COUNT * 2:
            increment()
            count2 += 1
        
        if remaining <= 1:
            players[current_turn].place = remaining
            for i in range(PLAYER_COUNT):
                FITNESS[i] = 4 - players[i].place
            return current_turn
    
    count += 1
    if count >= STALEMATE:
        FITNESS = fitness_for_draw()
        return 10 #10 will be the draw result
    
    return -1



"""


def main():
    outcome = -1
    
    while outcome == -1:        
        outcome = turn()
    
    print(FITNESS)
    
    
    if outcome == 10:
        print("Draw")


if __name__ == "__main__":
    main()
    print(time.time() - time1)
    
    
"""


def run_game(pop, config): #renamed so as to not be confused with neat.Population.run()
    #you need to have defined the population before so that pop is the networks themselves, not the population object, i.e. takes list(pop.population.items())
     
    players.clear()
    
    for i in range(len(pop)):
        #I think we're going to have to fuck around with the genome ids here, hopefully doesnt matter...
        #so instead of using genome_id, we just use the number of objects in the list so we iterate through with i, means we don't have to worry about the indexing
        
        net = neat.nn.FeedForwardNetwork.create(pop[i][1], config)
        players.append(NetworkPlayer(net))
        network.set_position(i, players[i].pos) #when doing this later, I think we'll have to do ((genome_id -1) % 4)
        network.set_money(i, players[i].money)
    
    
    outcome = -1
    
    while outcome == -1:        
        outcome = turn()
    
    
    if outcome == 10:
        print("Draw")
        
    return FITNESS



if __name__ == "__main__":


    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-monopoly')
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
    
    
    
    p = neat.Population(config)
    test = list(p.population.items())
    
    print(run_game(test, config))
    
    print(time.time() - time1)






    

