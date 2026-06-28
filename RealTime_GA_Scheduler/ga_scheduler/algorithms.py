"""
Multi-Algorithm Scheduler Integration
Supports Random, Round Robin, HEFT, PSO, GA, DQN, and GA-DQN
for comparison with existing GA baseline.
"""

import random
from typing import List, Dict, Tuple
from .models import Task, VM
from .simulator import simulate_schedule
from .utils import topo_order_from_tasks
from .ga import ga_optimize

Assignment = Dict[str, Tuple[str, int]]

# ----------------- BASIC SCHEDULERS -----------------

class RandomScheduler:
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms

    def schedule(self):
        result = {}
        vm_ids = list(self.vms.keys())
        for t in self.tasks:
            vm = random.choice(vm_ids)
            core = random.randrange(self.vms[vm].cores)
            result[t.id] = (vm, core)
        return result


class RoundRobinScheduler:
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms

    def schedule(self):
        result = {}
        vm_ids = list(self.vms.keys())
        idx = 0
        for t in self.tasks:
            vm = vm_ids[idx % len(vm_ids)]
            core = idx % self.vms[vm].cores
            result[t.id] = (vm, core)
            idx += 1
        return result


class HEFTScheduler:
    """Simplified HEFT scheduler (based on earliest finish time)."""
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms

    def schedule(self):
        topo = topo_order_from_tasks(self.tasks)
        assign = {}
        for tid in topo:
            t = next(x for x in self.tasks if x.id == tid)
            best_vm, best_core, best_time = None, None, float('inf')
            for vm_id, vm in self.vms.items():
                for c in range(vm.cores):
                    exec_time = t.comp / vm.core_speed(c)
                    if exec_time < best_time:
                        best_vm, best_core, best_time = vm_id, c, exec_time
            assign[t.id] = (best_vm, best_core)
        return assign


class PSOScheduler:
    """Placeholder for PSO (uses random exploration)."""
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms

    def schedule(self):
        result = {}
        vm_ids = list(self.vms.keys())
        for t in self.tasks:
            vm = random.choice(vm_ids)
            core = random.randrange(self.vms[vm].cores)
            result[t.id] = (vm, core)
        return result


# ----------------- EXISTING GA -----------------

class GAScheduler:
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms

    def schedule(self):
        best_assign, _ = ga_optimize(self.tasks, self.vms)
        return best_assign


# ----------------- PLACEHOLDER DQN / GA-DQN -----------------

class DQNScheduler:
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms
    def schedule(self):
        # Simulated output until DQN model implemented
        rs = RandomScheduler(self.tasks, self.vms)
        return rs.schedule()


class GADQNScheduler:
    def __init__(self, tasks, vms):
        self.tasks = tasks
        self.vms = vms
    def schedule(self):
        # Placeholder hybrid logic: run GA then random fine-tuning
        best_assign, _ = ga_optimize(self.tasks, self.vms)
        # Small mutation to simulate adaptive improvement
        for t in random.sample(self.tasks, k=max(1, len(self.tasks)//4)):
            vm = random.choice(list(self.vms.keys()))
            core = random.randrange(self.vms[vm].cores)
            best_assign[t.id] = (vm, core)
        return best_assign


# ----------------- COMPARISON FUNCTION -----------------

def compare_all_algorithms(tasks: List[Task], vms: Dict[str, VM], selected_algos=None):
    all_algos = {
        "Random": RandomScheduler,
        "RoundRobin": RoundRobinScheduler,
        "HEFT": HEFTScheduler,
        "PSO": PSOScheduler,
        "GA": GAScheduler,
        "DQN": DQNScheduler,
        "GA-DQN": GADQNScheduler,
    }

    if selected_algos:
        algos = {k: v for k, v in all_algos.items() if k in selected_algos}
    else:
        algos = all_algos

    results = {}
    for name, Algo in algos.items():
        scheduler = Algo(tasks, vms)
        assignment = scheduler.schedule()
        makespan, cost, comm = simulate_schedule(tasks, vms, assignment)
        results[name] = {
            "makespan": round(makespan, 3),
            "cost": round(cost, 3),
            "comm_time": round(comm, 3),
        }
    return results
