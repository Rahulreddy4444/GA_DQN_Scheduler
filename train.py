from GA_DQN_Scheduler.utils import create_workflow
from GA_DQN_Scheduler.ga_module import evolve
from GA_DQN_Scheduler.dqn_agent import DQNAgent
import numpy as np, random, torch
import matplotlib.pyplot as plt
from tqdm import tqdm

NUM_VMS = 10
agent = DQNAgent(state_dim=12, action_dim=NUM_VMS)
rewards, epsilons = [], []

for ep in tqdm(range(250)):
    wf = create_workflow(random.randint(5,10))
    best_scheme, exec_time = evolve(wf, generations=20)
    qos = random.uniform(0.5, 2.0)
    vm_waits = np.random.rand(NUM_VMS)
    state = np.concatenate(([exec_time, qos], vm_waits))
    action = agent.act(state)
    cost = random.uniform(0.3, 1.0)
    reward = (1 + 1/cost)*np.exp(qos/exec_time) - 1 if exec_time <= qos else (1 + cost)*np.log(qos/exec_time)
    next_state = np.concatenate(([exec_time, qos], vm_waits + np.random.rand(NUM_VMS)*0.1))
    agent.remember(state, action, reward, next_state, False)
    agent.replay()
    rewards.append(reward)
    epsilons.append(agent.epsilon)

# Plot rewards and epsilon decay
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(rewards)
plt.title("Training Rewards")

plt.subplot(1,2,2)
plt.plot(epsilons)
plt.title("Epsilon Decay")
plt.show()

# Save model
torch.save(agent.model.state_dict(), "GA_DQN_Scheduler/models/dqn_model.pkl")
print("✅ Model saved to GA_DQN_Scheduler/models/dqn_model.pkl")
