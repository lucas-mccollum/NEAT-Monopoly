class NetInputs:
    
    """
    This class will store the information from the board in a form that can be used by the neural network. 
    I **believe** that there will be 127 inputs to the network, which is more than was initially anticipated. 
    They will be:
        
        turn: first four inputs to denote which player is active (four entries)
        pos: next four inputs to denote where each player is (four entries)
        money: next four inputs, each player's money (four entries)
        goj: whether each player has a goj card (four entries)
        jail: if the player is in jail 
        owner: who owns each property (28 entries)
        mortgaged: if the property is mortgaged (28 entries)
        houses: how many houses on each property (22 entries)
        choice: enables players to select which properties to trade (28 entries)
        offer: how much money a player is willing to exchange for a property (one entry)
        
    
    A few notes: 
        
        - You can have more than one goj card, so that's why the value has to be normalised 
        - All values are normalised to keep them between 0 and 1
        - I don't actually know if we need to clamp them because I think NEAT-Python does it anyway but we'll do 
        it just to be safe 
        
    
    
    """
    
    turn = 0
    pos = 4
    money = 8
    goj = 12
    jail = 16 
    owner = 20
    mortgaged = 48
    houses = 76
    choice = 98
    offer = 126
    
    PROPERTIES = [-1, 0, -1, 1, -1, 2, 3, -1, 4, 5,
                  -1, 6, 7, 8, 9, 10, 11, -1, 12, 13,
                  -1, 14, -1, 15, 16, 17, 18, 19, 20,
                  21, -1, 22, 23, -1, 24, 25, -1, 26, 
                  -1, 27]
    
    HOUSES = [-1, 0, -1, 1, -1, -1, 2, -1, 3, 4,
              -1, 5, -1, 6, 7, -1, 8, -1, 9, 10,
              -1, 11, -1, 12, 13, -1, 14, 15, -1,
              16, -1, 17, 18, -1, 19, -1, -1, 20, 
              -1, 21]
    
    
    def __init__(self):
        
        self.inputs = [0] * 127
        
    def reset(self):
        self.inputs = [0] * 127
        
    def set_position(self, player, position):
        
        new_pos = position / 40        
        self.inputs[NetInputs.pos + player] = max(0, min(new_pos, 1))
    
    def set_jail(self, player, state):
        
        self.inputs[NetInputs.jail + player] = state
        
    def set_choice(self, index):
        
        self.inputs[NetInputs.choice + NetInputs.PROPERTIES[index]] = 1

    def clear_choices(self): #this is used before any trade suggestions are made
        
        for i in range(NetInputs.choice, NetInputs.choice + 29):
            self.inputs[i] = 0
            
    def set_context(self, money):
        
        self.inputs[NetInputs.offer] = money

    def set_money(self, player, money): #the reverse of this will be done in the player class
        
        new_money = money / 5000
        self.inputs[NetInputs.money + player] = max(0, min(new_money, 1))

    def set_cards(self, player, cards):
        
        if cards >= 1:
            self.inputs[NetInputs.goj + player] = 1
        
        else:
            self.inputs[NetInputs.goj + player] = 0
    
    def set_mortgaged(self, prop_id, state):
        
        self.inputs[NetInputs.mortgaged + NetInputs.PROPERTIES[prop_id]] = state
    
    def set_houses(self, prop_id, houses):
        
        new_houses = houses / 5
        self.inputs[NetInputs.houses + NetInputs.HOUSES[prop_id]] = max(0, min(new_houses, 1))
        
    def set_turn(self, player):
        
        for i in range(4):
            self.inputs[i] = 0
        
        self.inputs[player] = 1
    
    def set_owner(self, prop_id, state):
        
        self.inputs[NetInputs.owner + NetInputs.PROPERTIES[prop_id]] = (state + 1) / 4









