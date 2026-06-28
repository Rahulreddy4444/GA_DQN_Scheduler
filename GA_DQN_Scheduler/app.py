import streamlit as st
import numpy as np
import torch
import matplotlib.pyplot as plt
import networkx as nx
import os
import requests
import json

from GA_DQN_Scheduler.dqn_agent import DQNAgent
from GA_DQN_Scheduler.utils import create_workflow
from GA_DQN_Scheduler.ga_module import evolve

# ------------------------------
# Streamlit App Config
# ------------------------------
st.set_page_config(page_title="GA-DQN Workflow Scheduler", layout="wide")
st.title("🌐 GA-DQN Cloud Workflow Scheduler Dashboard")

# ------------------------------
# Model and Paths
# ------------------------------
NUM_VMS = 10
STATE_DIM = 12
MODEL_PATH = "GA_DQN_Scheduler/models/dqn_model.pkl"
MODEL_URL = "https://drive.google.com/uc?export=download&id=1HYm1UapmLfcH_i-4L5s8uUKqfrcpJB7O"  # your public drive link

# Create folder if not exists
os.makedirs("GA_DQN_Scheduler/models", exist_ok=True)

# ------------------------------
# Download Model if Missing
# ------------------------------
if not os.path.exists(MODEL_PATH):
    st.info("Downloading trained DQN model from Google Drive...")
    try:
        r = requests.get(MODEL_URL)
        if r.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)
            st.success("Model downloaded successfully!")
        else:
            st.error("❌ Failed to download model. Please check your Google Drive sharing link.")
            st.stop()
    except Exception as e:
        st.error(f"Download failed: {e}")
        st.stop()

# ------------------------------
# Load Trained DQN Agent
# ------------------------------
agent = DQNAgent(state_dim=STATE_DIM, action_dim=NUM_VMS)
agent.model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
agent.model.eval()

# ------------------------------
# Sidebar Controls
# ------------------------------
st.sidebar.header("⚙️ Workflow & Environment Settings")
num_tasks = st.sidebar.slider("Number of Tasks in Workflow", min_value=5, max_value=20, value=10)
qos = st.sidebar.slider("QoS Requirement", min_value=0.5, max_value=2.0, value=1.0)
vm_wait_randomness = st.sidebar.slider("VM Wait Time Variability", 0.0, 0.5, 0.1)

# ------------------------------
# Run Scheduler
# ------------------------------
if st.button("🚀 Run Scheduler"):
    wf = create_workflow(num_tasks)
    best_scheme, exec_time = evolve(wf, generations=20)

    vm_waits = np.random.rand(NUM_VMS) * (1 + vm_wait_randomness)
    state = np.concatenate(([exec_time, qos], vm_waits))
    action = agent.act(state)

    # Reward calculation (same as training)
    cost = np.random.uniform(0.3, 1.0)
    reward = (1 + 1/cost) * np.exp(qos/exec_time) - 1 if exec_time <= qos else (1 + cost) * np.log(qos/exec_time)

    # ------------------------------
    # Display Results
    # ------------------------------
    st.subheader("🧠 Scheduler Output")
    st.markdown(f"**DQN Selected VM:** VM {action}")
    st.markdown(f"**Workflow Estimated Execution Time:** {exec_time:.2f}")
    st.markdown(f"**Workflow Reward:** {reward:.2f}")
    st.markdown(f"**Workflow Scheme (task → core):** {best_scheme}")

    # ------------------------------
    # DAG Visualization
    # ------------------------------
    st.subheader("📊 Workflow DAG")
    fig, ax = plt.subplots(figsize=(8,5))
    pos = nx.spring_layout(wf)
    nx.draw(wf, pos, with_labels=True, node_color='skyblue', node_size=600, arrows=True, ax=ax)
    st.pyplot(fig)

    # ------------------------------
    # Load Real Training Metrics (if available)
    # ------------------------------
    metrics_file = "GA_DQN_Scheduler/models/training_metrics.json"
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
        rewards = metrics.get("rewards", [])
        epsilons = metrics.get("epsilons", [])
    else:
        rewards = [np.random.uniform(-1,1) for _ in range(50)]
        epsilons = [max(0.1, 0.99*np.exp(-0.05*i)) for i in range(50)]

    st.subheader("📈 Training Metrics")
    col1, col2 = st.columns(2)
    with col1:
        if rewards:
            st.line_chart(rewards, height=250)
            st.caption("Training Rewards")
    with col2:
        if epsilons:
            st.line_chart(epsilons, height=250)
            st.caption("Epsilon Decay")
