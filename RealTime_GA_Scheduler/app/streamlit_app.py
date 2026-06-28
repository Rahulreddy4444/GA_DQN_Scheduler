# # app/streamlit_app.py
# import streamlit as st
# import matplotlib.pyplot as plt
# import networkx as nx
# from ga_scheduler.utils import generate_random_workflow
# from ga_scheduler.models import VM
# from ga_scheduler.ga import ga_optimize
# from ga_scheduler.simulator import simulate_schedule
# # --- Multi-Algorithm Comparison ---
# from ga_scheduler.algorithms import compare_all_algorithms

# st.markdown("## ⚖️ Compare Multiple Scheduling Algorithms")

# selected = st.multiselect(
#     "Select algorithms to compare:",
#     ["Random", "RoundRobin", "HEFT", "PSO", "GA", "DQN", "GA-DQN"],
#     default=["GA", "GA-DQN", "HEFT"]
# )

# # --- Page Config ---
# st.set_page_config(page_title="Real-Time GA Scheduler", layout="wide")

# st.title("🧬 Real-Time Genetic Algorithm Scheduler for Cloud Workflows")
# st.markdown("This demo lets you generate a random workflow (DAG), visualize it, and schedule it across multiple VMs using GA.")

# # Sidebar: Parameters
# st.sidebar.header("⚙️ Configuration")
# num_tasks = st.sidebar.slider("Number of Tasks", 4, 20, 8)
# edge_prob = st.sidebar.slider("Edge Probability", 0.1, 0.9, 0.3)
# pop_size = st.sidebar.slider("Population Size", 10, 100, 30)
# generations = st.sidebar.slider("Generations", 5, 50, 20)
# mut_prob = st.sidebar.slider("Mutation Probability", 0.0, 0.5, 0.15)
# alpha = st.sidebar.number_input("Weight α (Makespan)", 0.0, 5.0, 1.0)
# beta = st.sidebar.number_input("Weight β (Cost)", 0.0, 5.0, 0.3)
# gamma = st.sidebar.number_input("Weight γ (Comm)", 0.0, 5.0, 0.2)

# # VM Setup
# st.sidebar.subheader("💻 VM Configuration")
# vm_count = st.sidebar.slider("Number of VMs", 2, 5, 3)

# if st.sidebar.button("🎲 Generate Workflow"):
#     g, tasks = generate_random_workflow(num_tasks=num_tasks, edge_prob=edge_prob)
#     st.session_state['workflow'] = (g, tasks)

# # Display workflow
# if 'workflow' in st.session_state:
#     g, tasks = st.session_state['workflow']
#     st.subheader("📊 Generated Workflow DAG")

#     pos = nx.spring_layout(g, seed=42)
#     plt.figure(figsize=(5, 4))
#     nx.draw(g, pos, with_labels=True, node_color="skyblue", node_size=1500, arrowsize=20)
#     st.pyplot(plt)

#     st.markdown("### Task Details")
#     for t in tasks:
#         st.markdown(f"- **{t.id}** — comp={t.comp:.1f}, preds={t.preds}, type={t.ttype}")

#     # Prepare VM dictionary
#     vms = {}
#     for i in range(vm_count):
#         vid = f"VM{i+1}"
#         vms[vid] = VM(
#             id=vid,
#             speeds=[500, 300, 200],
#             cores=2,
#             cost_rate=1.0 + 0.3*i,
#             vtype="general",
#             current_wait=0.2*i
#         )

#     if st.button("🚀 Run GA Scheduler"):
#         with st.spinner("Running Genetic Algorithm..."):
#             best_assign, score = ga_optimize(
#                 tasks, vms,
#                 pop_size=pop_size, generations=generations,
#                 mut_prob=mut_prob,
#                 alpha=alpha, beta=beta, gamma=gamma
#             )

#             makespan, cost, comm = simulate_schedule(tasks, vms, best_assign)
#             st.success("Scheduling Complete ✅")

#             # Results
#             st.markdown("### 🧾 Results")
#             st.markdown(f"**Best Fitness:** {score:.3f}")
#             st.markdown(f"**Makespan:** {makespan:.3f} s")
#             st.markdown(f"**Total Cost:** {cost:.3f}")
#             st.markdown(f"**Total Communication Delay:** {comm:.3f} s")

#             st.markdown("### Task → VM Assignment")
#             for t in tasks:
#                 vm, core = best_assign[t.id]
#                 st.markdown(f"- {t.id} → **{vm} (core {core})**")

# else:
#     st.info("👈 Configure and click **'Generate Workflow'** in the sidebar to start.")

# if st.button("📈 Run Comparison"):
#     with st.spinner("Running all selected algorithms..."):
#         results = compare_all_algorithms(tasks, vms, selected_algos=selected)
#         import pandas as pd
#         df = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Algorithm'})
#         st.dataframe(df)

#         # --- Visualization ---
#         import matplotlib.pyplot as plt
#         fig, ax = plt.subplots(1, 3, figsize=(12, 4))
#         ax[0].bar(df['Algorithm'], df['makespan']); ax[0].set_title("Makespan")
#         ax[1].bar(df['Algorithm'], df['cost']); ax[1].set_title("Execution Cost")
#         ax[2].bar(df['Algorithm'], df['comm_time']); ax[2].set_title("Communication Time")
#         for a in ax: a.set_xticklabels(df['Algorithm'], rotation=45, ha='right')
#         st.pyplot(fig)


# app/streamlit_app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from ga_scheduler.utils import generate_random_workflow
from ga_scheduler.models import VM
from ga_scheduler.ga import ga_optimize
from ga_scheduler.simulator import simulate_schedule
from ga_scheduler.algorithms import compare_all_algorithms

# --- PAGE CONFIG ---
st.set_page_config(page_title="Real-Time GA Scheduler", layout="wide")

# --- HEADER ---
st.title("🧬 Real-Time Workflow Scheduling System")
st.markdown("""
This app demonstrates real-time workflow scheduling for cloud environments.
You can generate a random DAG workflow, run the Genetic Algorithm (GA) scheduler, 
and compare multiple algorithms such as **GA-DQN**, **DQN**, **HEFT**, **PSO**, and more.
""")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Workflow & Algorithm Parameters")
num_tasks = st.sidebar.slider("Number of Tasks", 4, 20, 8)
edge_prob = st.sidebar.slider("Edge Probability", 0.1, 0.9, 0.3)
pop_size = st.sidebar.slider("GA Population Size", 10, 100, 30)
generations = st.sidebar.slider("GA Generations", 5, 50, 20)
mut_prob = st.sidebar.slider("Mutation Probability", 0.0, 0.5, 0.15)
alpha = st.sidebar.number_input("Weight α (Makespan)", 0.0, 5.0, 1.0)
beta = st.sidebar.number_input("Weight β (Cost)", 0.0, 5.0, 0.3)
gamma = st.sidebar.number_input("Weight γ (Communication)", 0.0, 5.0, 0.2)

# --- VM CONFIGURATION ---
st.sidebar.subheader("💻 VM Configuration")
vm_count = st.sidebar.slider("Number of VMs", 2, 5, 3)

# --- GENERATE WORKFLOW ---
if st.sidebar.button("🎲 Generate Workflow"):
    g, tasks = generate_random_workflow(num_tasks=num_tasks, edge_prob=edge_prob)
    st.session_state['workflow'] = (g, tasks)
    st.success("✅ Workflow Generated!")

# --- DISPLAY WORKFLOW ---
if 'workflow' in st.session_state:
    g, tasks = st.session_state['workflow']
    st.subheader("📊 Generated Workflow DAG")

    pos = nx.spring_layout(g, seed=42)
    plt.figure(figsize=(5, 4))
    nx.draw(g, pos, with_labels=True, node_color="skyblue", node_size=1500, arrowsize=20)
    st.pyplot(plt)

    st.markdown("### Task Details")
    for t in tasks:
        st.markdown(f"- **{t.id}** — comp={t.comp:.1f}, preds={t.preds}, type={t.ttype}")

    # --- VM SETUP ---
    vms = {}
    for i in range(vm_count):
        vid = f"VM{i+1}"
        vms[vid] = VM(
            id=vid,
            speeds=[500, 300, 200],
            cores=2,
            cost_rate=1.0 + 0.3*i,
            vtype="general",
            current_wait=0.2*i
        )

    # --- RUN GA SCHEDULER ---
    if st.button("🚀 Run GA Scheduler"):
        with st.spinner("Running Genetic Algorithm..."):
            best_assign, score = ga_optimize(
                tasks, vms,
                pop_size=pop_size, generations=generations,
                mut_prob=mut_prob,
                alpha=alpha, beta=beta, gamma=gamma
            )

            makespan, cost, comm = simulate_schedule(tasks, vms, best_assign)
            st.success("✅ Scheduling Complete")

            # --- RESULTS ---
            st.markdown("### 🧾 GA Results")
            st.markdown(f"**Best Fitness:** {score:.3f}")
            st.markdown(f"**Makespan:** {makespan:.3f} s")
            st.markdown(f"**Total Cost:** {cost:.3f}")
            st.markdown(f"**Communication Delay:** {comm:.3f} s")

            st.markdown("### Task → VM Assignment")
            for t in tasks:
                vm, core = best_assign[t.id]
                st.markdown(f"- {t.id} → **{vm} (core {core})**")

    # --- MULTI-ALGORITHM COMPARISON ---
    st.markdown("---")
    st.markdown("## ⚖️ Multi-Algorithm Comparison")

    selected = st.multiselect(
        "Select algorithms to compare:",
        ["Random", "RoundRobin", "HEFT", "PSO", "GA", "DQN", "GA-DQN"],
        default=["GA", "GA-DQN", "HEFT"]
    )

    if st.button("📈 Run Comparison"):
        with st.spinner("Running all selected algorithms..."):
            results = compare_all_algorithms(tasks, vms, selected_algos=selected)
            df = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Algorithm'})
            st.dataframe(df)

            # --- VISUALIZATION ---
            fig, ax = plt.subplots(1, 3, figsize=(12, 4))
            ax[0].bar(df['Algorithm'], df['makespan']); ax[0].set_title("Makespan")
            ax[1].bar(df['Algorithm'], df['cost']); ax[1].set_title("Execution Cost")
            ax[2].bar(df['Algorithm'], df['comm_time']); ax[2].set_title("Communication Time")

            for a in ax:
                a.set_xticklabels(df['Algorithm'], rotation=45, ha='right')

            st.pyplot(fig)

else:
    st.info("👈 Configure and click **'Generate Workflow'** in the sidebar to start.")
