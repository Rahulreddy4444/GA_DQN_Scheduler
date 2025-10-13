import streamlit as st
import numpy as np
import torch
import matplotlib.pyplot as plt
import networkx as nx

from GA_DQN_Scheduler.dqn_agent import DQNAgent
from GA_DQN_Scheduler.utils import create_workflow
from GA_DQN_Scheduler.ga_module import evolve

st.set_page_config(page_title="GA-DQN Workflow Scheduler", layout="wide")
st.title("🌐 GA-DQN Cloud Workflow Scheduler Dashboard")

# ------------------------------
# Load trained DQN agent
# ------------------------------
NUM_VMS = 10
STATE_DIM = 12
agent = DQNAgent(state_dim=STATE_DIM, action_dim=NUM_VMS)
agent.model.load_state_dict(torch.load("GA_DQN_Scheduler/models/dqn_model.pkl"))
agent.model.eval()

# ------------------------------
# Sidebar controls
# ------------------------------
st.sidebar.header("Workflow & Environment Settings")
num_tasks = st.sidebar.slider("Number of Tasks in Workflow", min_value=5, max_value=20, value=10)
qos = st.sidebar.slider("QoS Requirement", min_value=0.5, max_value=2.0, value=1.0)
vm_wait_randomness = st.sidebar.slider("VM Wait Time Variability", 0.0, 0.5, 0.1)

# ------------------------------
# Generate workflow
# ------------------------------
if st.button("Run Scheduler"):
    wf = create_workflow(num_tasks)
    best_scheme, exec_time = evolve(wf, generations=20)
    vm_waits = np.random.rand(NUM_VMS) * (1 + vm_wait_randomness)
    state = np.concatenate(([exec_time, qos], vm_waits))
    action = agent.act(state)

    # Reward calculation (same as training)
    cost = np.random.uniform(0.3, 1.0)
    reward = (1 + 1/cost) * np.exp(qos/exec_time) - 1 if exec_time <= qos else (1 + cost) * np.log(qos/exec_time)

    # ------------------------------
    # Display results
    # ------------------------------
    st.subheader("Scheduler Output")
    st.markdown(f"**DQN Selected VM:** VM {action}")
    st.markdown(f"**Workflow Estimated Execution Time:** {exec_time:.2f}")
    st.markdown(f"**Workflow Reward:** {reward:.2f}")
    st.markdown(f"**Workflow Scheme (task -> core):** {best_scheme}")

    # ------------------------------
    # DAG visualization
    # ------------------------------
    st.subheader("Workflow DAG")
    fig, ax = plt.subplots(figsize=(8,5))
    pos = nx.spring_layout(wf)
    nx.draw(wf, pos, with_labels=True, node_color='skyblue', node_size=600, arrows=True, ax=ax)
    st.pyplot(fig)

    # ------------------------------
    # Simulate reward & epsilon charts
    # ------------------------------
    st.subheader("Simulated Training Metrics")
    rewards = [np.random.uniform(-1,1) for _ in range(50)]
    epsilons = [max(0.1, 0.99*np.exp(-0.05*i)) for i in range(50)]
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(rewards, height=250)
        st.caption("Training Rewards (Simulated)")
    with col2:
        st.line_chart(epsilons, height=250)
        st.caption("Epsilon Decay (Simulated)")
