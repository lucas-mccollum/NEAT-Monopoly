import Board
import os
import neat
import random
import visualize

#first define a function that can split the list into n equal, random groups
def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]

def eval_genomes(pop, config):
    current_pool = pop
    n = 0
    
    while len(current_pool) > 1:
        print(f"Round {n}")
        no_groups = int(len(current_pool) / 4) #find how many groups we have to split our population into
        groups = partition(current_pool, no_groups) #randomise and split
        
        new_pool = []
        
        for group in groups: #the items in group are network objects so you have to do the whole run thing in the board
            Board.outcome = -1
            fitness = Board.run_game(group, config)
            current_genome = 0
            for genome_id, genome in group:
                genome.fitness = fitness[current_genome] + n ** 2
                current_genome += 1
                
                #this gives us all the group fitnesses
            
            #now we need to find the best genome
            max_fitness = 0
            best_genome = (0, 0)
            for genome_id, genome in group:
                if genome.fitness > max_fitness:
                    max_fitness = genome.fitness
                    best_genome = (genome_id, genome)
            
            new_pool.append(best_genome)
        
        current_pool = new_pool
        n += 1
    
    for genome_id, genome in current_pool:
        genome.fitness = n ** 2

    
                    
                    

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-monopoly')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

#p = list(neat.Population(config).population.items())
#eval_genomes(p, config)

p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(5))


winner = p.run(eval_genomes, 3)

visualize.plot_stats(stats, ylog=False, view=True)
visualize.plot_species(stats, view=True)





