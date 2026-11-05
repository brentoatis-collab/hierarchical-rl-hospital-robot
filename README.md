> **Applied AI portfolio project by Brent Oatis, MBA**
> Applying hierarchical reinforcement learning to hospital logistics and task planning.

# CST643 Week 5 – Hierarchical Reinforcement Learning Hospital Robot

## Project Overview
This project implements a **Hierarchical Reinforcement Learning (HRL)** agent for a hospital robot operating in a GridWorld environment. The robot is designed to navigate hospital rooms, deliver medicine to patients, and exit efficiently after completing its tasks.

Rather than learning the full task as one large problem, the system uses **hierarchical decomposition**:
- a **high-level meta-controller** decides what sub-goal to pursue
- **low-level policies** decide how to execute each sub-task

This architecture improves structure, coordination, and task efficiency compared to a flat reinforcement learning approach.

---

## Objective
The objective of this assignment is to demonstrate how HRL can improve learning efficiency by decomposing a complex task into smaller, manageable sub-tasks. The hospital robot must:

- navigate through a GridWorld hospital layout
- identify patients who need medicine
- deliver medicine successfully
- exit the hospital after all deliveries are complete

---

## Environment Design
The environment is implemented in `env_hospital.py` as a custom GridWorld.

### Key environment elements
- **Robot start position**
- **Patient locations**
- **Exit location**
- **Walls / movement constraints**

### Action space
The robot can perform the following actions:
- `0` = up
- `1` = down
- `2` = left
- `3` = right
- `4` = deliver medicine

### Reward structure
The reward system was designed to encourage efficient behavior:
- `-1` for valid movement
- `-5` for hitting a wall or invalid boundary
- `+15` for successful medicine delivery
- `-2` for invalid delivery attempts
- `+30` for successful exit after all deliveries
- `-10` for reaching the exit before completing all deliveries

---

## HRL Architecture

### High-Level Policy
Implemented in `meta_controller.py`

The meta-controller selects the next sub-goal based on the current state of the hospital environment. Its primary sub-goals are:
- navigate to patient
- deliver medicine
- exit hospital

### Low-Level Policies
Implemented in `low_level_policies.py`

These policies execute the actions required to complete the selected sub-goal:
- navigation policy
- delivery policy
- exit policy

### Training Loop
Implemented in `train_hrl.py`

The hierarchical training loop works as follows:
1. The meta-controller selects a sub-goal
2. The corresponding low-level policy executes actions
3. The environment returns updated state and reward
4. The system continues until the mission is completed or the episode terminates

### Evaluation
Implemented in `evaluate_hrl.py`

The model is evaluated using:
- **task completion time** measured by average steps
- **reward accumulation efficiency** measured by average reward
- **success rate** across multiple runs

---

## Project Files

```text
CST643_Week5_HRL_Hospital_Robot/
├── env_hospital.py
├── meta_controller.py
├── low_level_policies.py
├── train_hrl.py
├── evaluate_hrl.py
├── run_demo.py
├── requirements.txt
├── README.md
└── claude_conversation_log.md
```

## Installation

### 1. Create and activate virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run

### Demo the environment
```bash
python run_demo.py
```
### Train the HRL Agent
```bash
python train_hrl.py
```
### Evaluate Performance
```bash
python evaluate_hrl.py
```

---

## Results

The HRL hospital robot achieved stable performance across multiple evaluation runs.

### Final evaluation averages
- **Average Steps:** 22.4
- **Average Reward:** 36.4
- **Success Rate:** 100%

### Interpretation
These results show that:
- the agent converged consistently across runs
- the navigation and delivery logic became efficient after optimization
- the reward structure aligned well with the desired task behavior
- hierarchical decomposition improved decision-making and execution reliability

---

## Challenges and Optimization

The main challenge during development was inefficient navigation, which initially caused looping behavior and poor task completion.

### Problems observed
- high step counts
- negative rewards
- failure to complete sub-goals consistently

### Solutions applied
- improved navigation targeting logic
- reduced inefficient loops
- strengthened coordination between high-level and low-level policies

These optimizations significantly improved both task completion and reward performance.

---

## Key Insight

This project reinforced an important principle of HRL:

**Hierarchical structure improves organization, but performance still depends on precise execution at the policy level.**

---

## Repository

GitHub Repository:  
`https://github.com/brentoatis-collab/hierarchical-rl-hospital-robot`

---

## References

Dietterich, T. G. (1999). *Hierarchical reinforcement learning with the MAXQ value function decomposition*. arXiv. https://arxiv.org/abs/cs/9905014

GeeksforGeeks. (2024, August 30). *Hierarchical reinforcement learning (HRL) in AI*. https://www.geeksforgeeks.org/hierarchical-reinforcement-learning-hrl-in-ai/

Konidaris, G., & Barto, A. G. (2009). Skill discovery in continuous reinforcement learning domains using skill chaining. In Y. Bengio et al. (Eds.), *Advances in neural information processing systems* (Vol. 22). https://proceedings.neurips.cc/paper/2009/file/e0cf1f47118daebc5b16269099ad7347-Paper.pdf

Lazaric, A. (2012). Transfer in reinforcement learning: A framework and a survey. In M. Wiering & M. van Otterlo (Eds.), *Reinforcement learning: State-of-the-art* (pp. 143–173). Springer. https://doi.org/10.1007/978-3-642-27645-3_5
