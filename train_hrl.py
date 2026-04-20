import time
import numpy as np

from env_hospital import HospitalGridWorld
from meta_controller import HighLevelPolicy
from low_level_policies import LowLevelPolicies


def train_hrl_agent(episodes=50, render=False):
    """
    Train the HRL hospital robot.

    Workflow:
    1. Reset environment
    2. Meta-controller selects sub-goal
    3. Low-level policy executes action for that sub-goal
    4. Environment returns reward and next state
    5. Track performance metrics

    Returns:
    - episode_steps: list of steps per episode
    - episode_rewards: list of rewards per episode
    - avg_training_time: average episode runtime
    """
    env = HospitalGridWorld()
    meta_controller = HighLevelPolicy(
        patient_positions=env.patient_positions,
        exit_pos=env.exit_pos
    )
    low_level = LowLevelPolicies()

    episode_steps = []
    episode_rewards = []
    training_times = []

    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        start_time = time.time()

        while not done:
            robot_pos = env.robot_pos
            delivered_status = env.delivered

            # Step 1: High-level policy selects sub-goal
            subgoal = meta_controller.select_subgoal(robot_pos, delivered_status)

            # Step 2: Low-level policy decides action
            if subgoal == "navigate_to_patient":
                target_patient = meta_controller.get_next_undelivered_patient(delivered_status)
                action = low_level.navigate_to_target(
                    robot_pos=robot_pos,
                    target_pos=target_patient,
                    grid_size=env.grid_size,
                    walls=env.room_walls
                )

            elif subgoal == "deliver_medicine":
                action = low_level.deliver_medicine(
                    robot_pos=robot_pos,
                    patient_positions=env.patient_positions,
                    delivered_status=delivered_status
                )

                # Safety fallback if no valid deliver action found
                if action is None:
                    target_patient = meta_controller.get_next_undelivered_patient(delivered_status)
                    action = low_level.navigate_to_target(
                        robot_pos=robot_pos,
                        target_pos=target_patient,
                        grid_size=env.grid_size,
                        walls=env.room_walls
                    )

            elif subgoal == "exit_hospital":
                action = low_level.exit_hospital(
                    robot_pos=robot_pos,
                    exit_pos=env.exit_pos,
                    grid_size=env.grid_size,
                    walls=env.room_walls
                )

            elif subgoal == "mission_complete":
                break

            else:
                raise ValueError(f"Unknown subgoal: {subgoal}")

            # Step 3: Execute action in environment
            state, reward, done, info = env.step(action)
            total_reward += reward

            if render:
                print(f"Episode {episode + 1} | Subgoal: {subgoal} | Action: {action} | Reward: {reward}")
                env.render()

        end_time = time.time()
        episode_time = end_time - start_time

        episode_steps.append(env.steps)
        episode_rewards.append(total_reward)
        training_times.append(episode_time)

        print(
            f"Episode {episode + 1}/{episodes} | "
            f"Steps: {env.steps} | "
            f"Reward: {total_reward} | "
            f"Time: {episode_time:.4f}s"
        )

    avg_training_time = np.mean(training_times)

    print("\nTraining Complete")
    print(f"Average Steps: {np.mean(episode_steps):.2f}")
    print(f"Average Reward: {np.mean(episode_rewards):.2f}")
    print(f"Average Episode Time: {avg_training_time:.4f}s")

    return episode_steps, episode_rewards, avg_training_time


if __name__ == "__main__":
    train_hrl_agent(episodes=10, render=True)