import random 
import Board

#first define a function that can split the list into n equal, random groups
def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]

def eval_genomes(pop, config):
    
    current_pool = pop
    n = 0
    while len(current_pool) > 1: 
        
        print(current_pool)
        
        no_groups = int(len(current_pool) / 4) #find how many groups we have to split our population into
        groups = partition(current_pool, no_groups) #randomise and split
        #THIS IS WHERE YOU RUN THE GAMES, sort them into ascending order for each group
        new_group = [i[0] for i in groups]
        current_pool = new_group
        n += 1
    print(current_pool)
       



lst = random.sample(range(256), 256)
eval_genomes(lst, 0)

Board.main()

