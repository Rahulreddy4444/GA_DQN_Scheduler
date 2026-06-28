# GA_DQN_Scheduler

This repository contains two workflow-scheduling projects:

- `GA_DQN_Scheduler/` — GA-DQN scheduler implementation and entry scripts.
- `RealTime_GA_Scheduler/` — real-time GA scheduler with Streamlit dashboard.

## How to run the GA-DQN project

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install the GA-DQN dependencies:

```bash
pip install -r GA_DQN_Scheduler/requirements.txt
```

3. Run the app:

```bash
python GA_DQN_Scheduler/app.py
```

4. Run training:

```bash
python GA_DQN_Scheduler/train.py
```

## How to run the RealTime_GA_Scheduler project

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install the real-time scheduler dependencies:

```bash
pip install -r RealTime_GA_Scheduler/requirements.txt
```

3. Run the example scheduler:

```bash
python -m RealTime_GA_Scheduler.ga_scheduler.main
```

4. Start the Streamlit dashboard:

```bash
streamlit run RealTime_GA_Scheduler/app/streamlit_app.py
```

## Notes

- The root `.gitignore` should remain at the top level so it covers both projects.
- If you want, I can also add a `README` inside `GA_DQN_Scheduler/` to document only that subproject.

| GA-DQN | 3.1 | 5.0 |

### Key Observations

- RT-GA achieved the lowest makespan.
- Better adaptability under dynamic workloads.
- Eliminates expensive DRL training overhead.
- Efficient multi-VM resource utilization.
- Improved scheduling performance in real-time environments.

---

## Project Structure

```text
GA_DQN_Scheduler/
├── app.py
├── train.py
├── requirements.txt
├── dqn_agent.py
├── ga_module.py
├── utils.py
├── __init__.py
└── README.md
├── docs/
│   ├── final_report.pdf
│   └── Project_Presentation.pptx
RealTime_GA_Scheduler/
├── app/
│   └── streamlit_app.py
├── ga_scheduler/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── ga.py
│   ├── main.py
│   ├── models.py
│   ├── simulator.py
│   └── utils.py
├── experiments/
│   └── examples.ipynb
├── requirements.txt
└── README.md
```

---

## Research Contributions

This project introduces:

1. Real-Time Genetic Algorithm (RT-GA)
2. Dynamic VM Feedback Integration
3. Multi-VM Workflow Scheduling
4. Cost-Aware Resource Allocation
5. Adaptive Fitness Evaluation
6. Queue-Aware Scheduling Mechanism

---

## Future Work

- Fog Computing Integration
- Edge Computing Support
- Hybrid GA + Reinforcement Learning Models
- Predictive Resource Scheduling
- Large-Scale Cloud Deployment
- Multi-Agent Scheduling Systems

---

## Academic Information

### Project Title

**Cost-Aware Real-Time Multi-VM Workflow Scheduling in Cloud Environments using a Genetic Algorithm**

### Institution

**Motilal Nehru National Institute of Technology (MNNIT) Allahabad**

### Department

**Computer Science & Engineering**

### Project Type

**B.Tech Final Year Project**

### Supervisor

**Dr. Ashish Kumar Maurya**

---

## Team Members

- Danapana Rahul Reddy (20223078)
- Anurag Choudhary (20223046)
- Abhay Kumar (20223004)
- Akula Sri Subramania Mukesh (20223530)

---

## Acknowledgements

We sincerely thank **Dr. Ashish Kumar Maurya** for his valuable guidance, continuous support, and encouragement throughout the development of this project.

We also express our gratitude to the **Department of Computer Science & Engineering, MNNIT Allahabad**, for providing the opportunity and resources necessary to carry out this work.

---

## License

This project was developed as part of a B.Tech Final Year Project at NIT Allahabad and is intended for academic and research purposes.

---

### If you found this project interesting, consider giving it a star!
