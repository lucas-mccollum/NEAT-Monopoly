import Board

#first define a function that can split the list into n equal, random groups
def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]

def eval_genomes(pop, config):
    
    current_pool = pop
    n = 0
    while len(current_pool) > 1: 
        
        #for the moment, we're pretending we have a run method in Board
        
        
        no_groups = int(len(current_pool) / 4) #find how many groups we have to split our population into
        groups = partition(current_pool, no_groups) #randomise and split
        
        for group in groups:
            fitness = Board.run(group)
            for genome_id, genome in group:
                genome.fitness = n ** 2 
        
        new_group = [i[0] for i in groups]
        current_pool = new_group
        n += 1
    print(current_pool)
       

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-monopoly')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

p = neat.Population(config)

print(p.population)

"""


lst = random.sample(range(256), 256)
eval_genomes(lst, 0)

"""
