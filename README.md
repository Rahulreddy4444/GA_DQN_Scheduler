# Cost-Aware Real-Time Multi-VM Workflow Scheduling using Genetic Algorithm (RT-GA)

> 🎓 B.Tech Minor Project | Department of Computer Science & Engineering | National Institute of Technology (NIT) Allahabad

## Live Demo
 **Live Application:** https://realtime-ga-scheduler-bheknww9uspb7oyq9nuukm.streamlit.app/


## Project Report & Presentation

### Final Project Report

 [View Final Report](./docs/final_report.pdf)

### Project Presentation

 [View Presentation](./docs/Project_Presentation.pptx)

---

## Overview

Cloud workflow scheduling is a challenging optimization problem due to heterogeneous Virtual Machines (VMs), dynamic workloads, and conflicting objectives such as minimizing execution cost and completion time.

This project proposes a **Cost-Aware Real-Time Genetic Algorithm (RT-GA)** that dynamically schedules workflow tasks across multiple Virtual Machines while considering:

- Execution Time (Makespan)
- Resource Utilization
- Execution Cost
- Communication Cost
- Real-Time VM Waiting Time

Unlike traditional scheduling approaches, RT-GA continuously adapts to changing cloud conditions using real-time VM feedback, enabling efficient resource allocation and improved workflow execution.

---

## Problem Statement

Traditional workflow scheduling approaches suffer from several limitations:

- HEFT is static and cannot adapt to changing workloads.
- Standard Genetic Algorithms are computationally expensive.
- GA-DQN introduces significant training overhead.
- Existing solutions often allocate entire workflows to a single VM, limiting parallelism and scalability.

This project addresses these limitations by enabling:

- Multi-VM task allocation
- Real-time adaptation to VM states
- Cost-aware scheduling
- Fine-grained workflow execution
- Dynamic load balancing

---

## Objectives

- Integrate real-time VM state information into the Genetic Algorithm fitness function.
- Enable fine-grained task distribution across multiple VMs.
- Minimize workflow makespan and execution cost.
- Improve resource utilization.
- Maintain low computational overhead suitable for real-time deployment.

---

## Key Features

✔ Real-Time VM Feedback Integration

✔ Multi-VM Workflow Scheduling

✔ Cost-Aware Resource Allocation

✔ Genetic Algorithm Optimization

✔ Dynamic Fitness Evaluation

✔ Adaptive Mutation & Crossover

✔ Workflow DAG Processing

✔ Streamlit-Based Interactive Dashboard

✔ Multi-Core VM Scheduling

---

## System Architecture

The proposed RT-GA framework consists of three major layers:

### 1. Workflow Input Module
- Receives workflow DAG
- Parses task dependencies
- Performs topological sorting

### 2. RT-GA Scheduler
- Population Initialization
- Fitness Evaluation
- Selection
- Crossover
- Mutation
- Real-Time Feedback Integration

### 3. Cloud Infrastructure Layer
- Multiple Virtual Machines
- Multi-Core Execution Environment
- Dynamic Resource Monitoring

---

## RT-GA Workflow

1. Collect real-time VM statistics.
2. Initialize the population using random and heuristic seeding.
3. Simulate workflow execution.
4. Evaluate fitness based on:
   - Makespan
   - Execution Cost
   - Communication Cost
5. Apply:
   - Selection
   - Crossover
   - Mutation
6. Update VM states using real-time feedback.
7. Return the optimal task-to-VM mapping.

---

## Fitness Function

The optimization objective is:

F = αT + βC + γD

Where:

- **T** = Makespan
- **C** = Execution Cost
- **D** = Communication Cost

The fitness function dynamically incorporates VM waiting times and system load to improve scheduling decisions.

---

## Chromosome Representation

Each chromosome represents a task-to-VM-core mapping:

Task → VM → Core

Example:

Task1 → VM2 → Core1

Task2 → VM1 → Core3

Task3 → VM3 → Core2

This representation enables fine-grained scheduling and improved parallelism.

---

## Technologies Used

- Python
- Genetic Algorithms
- Cloud Computing Concepts
- Workflow Scheduling
- DAG Processing
- Streamlit
- NumPy
- Matplotlib

---

## Experimental Setup

### Virtual Machines

| VM | Processing Speed (MIPS) | Cost ($/unit time) |
|----|-------------------------|-------------------|
| VM1 | 1000 | 0.2 |
| VM2 | 1500 | 0.3 |
| VM3 | 2000 | 0.4 |

### GA Parameters

- Population Size: 10
- Generations: 15
- Mutation Rate: 0.1

---

## Results

| Method | Makespan (s) | Execution Cost ($) |
|----------|-------------|------------------|
| HEFT | 3.6 | 3.7 |
| RT-GA | 2.4 | 4.0 |
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
│
├── app.py
├── train.py
├── requirements.txt
├── GA_DQN_Scheduler/
│
├── docs/
│   ├── final_report.pdf
│   └── Project_Presentation.pptx
│
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

**B.Tech Minor Project**

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

This project was developed as part of a B.Tech Minor Project at NIT Allahabad and is intended for academic and research purposes.

---

### If you found this project interesting, consider giving it a star!
