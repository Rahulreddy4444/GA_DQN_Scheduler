import random
from .utils import create_workflow  # ← relative import works inside package

VM_CORES = [200, 300, 400]

def compute_exec_time(task_mips, core_speed, vm_type, wf_type):
    if vm_type != wf_type:
        return 2 * task_mips / core_speed
    return task_mips / core_speed

def fitness(individual, workflow, vm_type='memory'):
    total = 0
    for task_id, core_id in individual:
        task_mips = workflow.nodes[task_id]['compute']
        total += compute_exec_time(task_mips, VM_CORES[core_id], vm_type, 'memory')
    return total

def generate_individual(workflow):
    tasks = list(workflow.nodes())
    random.shuffle(tasks)
    return [(t, random.randint(0, len(VM_CORES)-1)) for t in tasks]

def evolve(workflow, generations=20, pop_size=10):
    population = [generate_individual(workflow) for _ in range(pop_size)]
    for _ in range(generations):
        population.sort(key=lambda ind: fitness(ind, workflow))
        new_pop = population[:2]  # elitism
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population[:5], 2)
            point = random.randint(1, len(p1)-1)
            child = p1[:point] + p2[point:]
            if random.random() < 0.2:  # mutation
                idx = random.randint(0, len(child)-1)
                child[idx] = (child[idx][0], random.randint(0, len(VM_CORES)-1))
            new_pop.append(child)
        population = new_pop
    best = min(population, key=lambda ind: fitness(ind, workflow))
    return best, fitness(best, workflow)
