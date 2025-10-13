import networkx as nx
import random

def create_workflow(num_tasks):
    """
    Generate a random DAG workflow with 'num_tasks' sub-tasks.
    Each node has a 'compute' value representing MIPS requirement.
    """
    G = nx.DiGraph()
    for i in range(num_tasks):
        G.add_node(i, compute=random.randint(20, 100))
    
    # Random edges ensuring DAG (no cycles)
    for i in range(num_tasks):
        for j in range(i+1, num_tasks):
            if random.random() < 0.3:
                G.add_edge(i, j)
    return G
