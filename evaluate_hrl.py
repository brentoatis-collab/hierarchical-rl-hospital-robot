import numpy as np

from env_hospital import HospitalGridWorld
from meta_controller import HighLevelPolicy
from low_level_policies import LowLevelPolicies


def evaluate_hrl_agent(episodes=20, render=False):
    """
    Evaluate the HRL hospital robot using:
    - average steps (task completion time)
    - average reward (reward accumulation efficiency)
    - success rate
    """
    env = HospitalGridWorld()
    meta_controller = HighLevelPolicy(
        patient_positions=env.patient_positions,
        exit_pos=env.exit_pos
    )
    low_level = LowLevelPolicies()

    total_steps = []
    total_rewards = []
    success_count = 0

    for episode in range(episodes):
        env.reset()
        done = False
        reward_sum = 0

        while not done:
            robot_pos = env.robot_pos
            delivered_status = env.delivered

            subgoal = meta_controller.select_subgoal(robot_pos, delivered_status)

            if subgoal == "navigate_to_patient":
                target = meta_controller.get_next_undelivered_patient(delivered_status)
                action = low_level.navigate_to_target(
                    robot_pos,
                    target,
                    env.grid_size,
                    env.room_walls
                )

            elif subgoal == "deliver_medicine":
                action = low_level.deliver_medicine(
                    robot_pos,
                    env.patient_positions,
                    delivered_status
                )

                if action is None:
                    target = meta_controller.get_next_undelivered_patient(delivered_status)
                    action = low_level.navigate_to_target(
                        robot_pos,
                        target,
                        env.grid_size,
                        env.room_walls
                    )

            elif subgoal == "exit_hospital":
                action = low_level.exit_hospital(
                    robot_pos,
                    env.exit_pos,
                    env.grid_size,
                    env.room_walls
                )

            elif subgoal == "mission_complete":
                break

            else:
                raise ValueError(f"Unknown subgoal: {subgoal}")

            _, reward, done, _ = env.step(action)
            reward_sum += reward

            if render:
                print(f"Episode {episode + 1} | Subgoal: {subgoal} | Action: {action} | Reward: {reward}")
                env.render()

        total_steps.append(env.steps)
        total_rewards.append(reward_sum)

        if all(env.delivered) and env.robot_pos == env.exit_pos:
            success_count += 1

    print("\n===== EVALUATION RESULTS =====")
    print(f"Average Steps: {np.mean(total_steps):.2f}")
    print(f"Average Reward: {np.mean(total_rewards):.2f}")
    print(f"Success Rate: {(success_count / episodes) * 100:.2f}%")

    return total_steps, total_rewards, success_count


if __name__ == "__main__":
    evaluate_hrl_agent(episodes=20, render=False)