# Claude Conversation Log – Week 5 HRL Hospital Robot

## Step 0 – Project Initialization

Prompt:
I am building a hospital robot using Hierarchical Reinforcement Learning (HRL) in a GridWorld environment. The system will include a high-level meta-controller and multiple low-level policies.

Action Taken:
Created project folder structure with separate modules for environment, meta-controller, policies, training loop, and evaluation.

Outcome:
Established a modular architecture aligned with HRL design principles.

## Step 1 – Hospital GridWorld Environment

Prompt:
Build the hospital environment first. The robot must navigate a 6x6 GridWorld, avoid walls, deliver medicine to two patients, and exit only after completing all deliveries.

Action Taken:
Created env_hospital.py with a HospitalGridWorld class, including state space, action space, reward structure, wall constraints, patient positions, and exit logic.

Outcome:
Established the environment foundation required for hierarchical reinforcement learning with clear movement rules and mission objectives.

## Step 2 – High-Level Meta-Controller

Prompt:
Design the high-level policy first. The meta-controller should observe which patients still need medicine and decide whether the robot should navigate to a patient, deliver medicine, or exit the hospital after all deliveries are completed.

Action Taken:
Created meta_controller.py with a HighLevelPolicy class that selects the next sub-goal based on delivery progress and robot position.

Outcome:
Established the top layer of the HRL hierarchy, separating task selection from low-level movement execution.

## Step 3 – Low-Level Policies

Prompt:
Build each low-level policy separately. The low-level policies should focus only on how to complete a selected sub-task, such as navigating to a patient, delivering medicine, or exiting the hospital.

Action Taken:
Created low_level_policies.py with methods for navigation, medicine delivery, and exit navigation. The navigation logic uses a simple greedy strategy with fallback movement options to avoid walls.

Outcome:
Established independent low-level execution policies that mirror the decomposition principles of hierarchical reinforcement learning.

## Step 4 – Training Loop Refinement (Debug & Optimization)

Prompt:
Improve the low-level navigation policy to ensure the agent can reliably reach sub-goals and avoid getting stuck in loops.

Action Taken:
Rewrote the navigate_to_target() function in low_level_policies.py to include:
- Strong directional bias toward target
- Valid move checking to avoid walls and boundaries
- Randomized fallback exploration to escape local traps

Additionally refined train_hrl.py to:
- Ensure proper sub-goal transitions from meta-controller
- Add fallback logic when delivery action is not valid
- Track episode steps, rewards, and timing for performance evaluation

Outcome:
The HRL agent successfully learned to:
- Navigate to patients
- Deliver medicine
- Exit the hospital

Performance improved significantly:
- Average Steps reduced from 100 → ~21–24
- Rewards shifted from negative → strongly positive
- Agent consistently completed full task sequence

## Step 5 – Evaluation Metrics Implementation

Prompt:
Evaluate the HRL agent using structured metrics suitable for analysis and presentation.

Action Taken:
Updated evaluate_hrl.py to:
- Include executable main block
- Run multiple evaluation episodes
- Track:
  • Task completion steps  
  • Total reward  
  • Success rate  

Handled Gym warning (non-blocking) and ensured evaluation output prints clean metrics.

Outcome:
Evaluation produced stable, presentation-ready results:

- Average Steps: 24.30  
- Average Reward: 32.70  
- Success Rate: 100%  

This confirms:
- Effective task decomposition
- Strong policy coordination
- Efficient reward structure
- Reliable hierarchical execution