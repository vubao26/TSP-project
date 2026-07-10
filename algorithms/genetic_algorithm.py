import numpy as np
import random
from tsp_utils_son import compute_tour_length

def genetic_algorithm(dist_matrix, pop_size=100, generations=400, p_crossover=0.85, p_mutation=0.1):
    """Thuật toán Di truyền giải bài toán TSP."""
    n = len(dist_matrix)
    
    def create_individual():
        ind = list(range(n))
        random.shuffle(ind)
        return ind
    
    population = [create_individual() for _ in range(pop_size)]
    
    def crossover(parent1, parent2):
        if random.random() > p_crossover:
            return parent1.copy(), parent2.copy()
        i, j = sorted(random.sample(range(n), 2))
        def fill_child(p1, p2):
            child = [None] * n
            child[i:j+1] = p1[i:j+1]
            p2_remain = [item for item in p2 if item not in child]
            idx = (j + 1) % n
            for item in p2_remain:
                while child[idx] is not None:
                    idx = (idx + 1) % n
                child[idx] = item
            return child
        return fill_child(parent1, parent2), fill_child(parent2, parent1)

    def mutate(individual):
        if random.random() < p_mutation:
            i, j = random.sample(range(n), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    best_len = float('inf')
    best_tour = None
    
    for gen in range(generations):
        fitness_scores = [1.0 / compute_tour_length(ind, dist_matrix) for ind in population]
        min_idx = np.argmax(fitness_scores)
        gen_best_len = compute_tour_length(population[min_idx], dist_matrix)
        
        if gen_best_len < best_len:
            best_len = gen_best_len
            best_tour = list(population[min_idx])
            
        total_fit = sum(fitness_scores)
        prob = [f / total_fit for f in fitness_scores]
        cum_prob = np.cumsum(prob)
        
        def select_one():
            r = random.random()
            for i, cp in enumerate(cum_prob):
                if r <= cp: return population[i]
            return population[-1]
            
        new_pop = [best_tour.copy()] # Giữ lại cá thể tinh hoa nhất
        while len(new_pop) < pop_size:
            p1 = select_one()
            p2 = select_one()
            c1, c2 = crossover(p1, p2)
            new_pop.append(mutate(c1))
            if len(new_pop) < pop_size:
                new_pop.append(mutate(c2))
        population = new_pop
        
    return best_tour, {"pop_size": pop_size, "generations": generations}