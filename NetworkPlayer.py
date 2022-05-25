import neat
import os
from settings import *
from MyEnums import *


class NetworkPlayer:
    
    def __init__(self, genome):
        
        self.genome = genome #this will be a genome defined by neat-python

        
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
        
        return houses
    
    def decide_build_house(self, index):
        
        output = self.genome.activate(network.inputs)
        houses = output[6] * 15
        
        return houses
    
    def decide_bid(self, index):
        
        output = self.genome.activate(network.inputs)
        offer = 5000 * output[7]
        
        return offer
    
    def decide_unmortgage(self, index):
        
        output = self.genome.activate(network.inputs)
        
        if output[8] > 0.5:
            
            return decision.YES
        
        return decision.NO
        
        
        







"""

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-monopoly')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

p = neat.Population(config)


def test(g, c):
    for genome_id, genome in g.population.items():
        net = neat.nn.FeedForwardNetwork.create(genome, c)
        print(net.activate([0] * 127))
        
test(p, config)


"""