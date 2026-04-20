import gym
import numpy as np
from gym import spaces


class HospitalGridWorld(gym.Env):
    """
    Hospital robot GridWorld environment.

    Mission:
    1. Navigate to patients who need medicine
    2. Deliver medicine
    3. Exit the hospital efficiently after deliveries

    Actions:
    0 = up
    1 = down
    2 = left
    3 = right
    4 = deliver

    Observation:
    [robot_row, robot_col, delivered_patient_1, delivered_patient_2]

    Rewards:
    -1 for valid movement
    -5 for hitting wall/boundary
    +15 for successful medicine delivery
    -2 for invalid delivery attempt
    +30 for successful exit after all deliveries
    -10 for reaching exit before all deliveries
    """

    def __init__(self, grid_size=6):
        super(HospitalGridWorld, self).__init__()

        self.grid_size = grid_size

        # Hospital layout
        self.start_pos = [0, 0]
        self.exit_pos = [5, 5]
        self.patient_positions = [[1, 4], [4, 2]]
        self.room_walls = {(1, 1), (2, 1), (3, 3), (4, 4)}

        # Action space: up, down, left, right, deliver
        self.action_space = spaces.Discrete(5)

        # Observation space:
        # robot row, robot col, patient1 delivered (0/1), patient2 delivered (0/1)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]),
            high=np.array([grid_size - 1, grid_size - 1, 1, 1]),
            dtype=np.int32
        )

        self.reset()

    def reset(self):
        """Reset environment to initial state."""
        self.robot_pos = self.start_pos.copy()
        self.delivered = [0, 0]
        self.steps = 0
        self.total_reward = 0
        return self._get_obs()

    def _get_obs(self):
        """Return current observation."""
        return np.array(
            [
                self.robot_pos[0],
                self.robot_pos[1],
                self.delivered[0],
                self.delivered[1],
            ],
            dtype=np.int32
        )

    def _all_medicines_delivered(self):
        """Check if all patients have received medicine."""
        return all(self.delivered)

    def _get_patient_index(self, position):
        """Return patient index if robot is on a patient location."""
        for i, patient_pos in enumerate(self.patient_positions):
            if position == patient_pos:
                return i
        return None

    def step(self, action):
        """Execute one environment step."""
        reward = 0
        done = False
        old_pos = self.robot_pos.copy()

        # Movement actions
        if action in [0, 1, 2, 3]:
            new_pos = self.robot_pos.copy()

            if action == 0:  # up
                new_pos[0] -= 1
            elif action == 1:  # down
                new_pos[0] += 1
            elif action == 2:  # left
                new_pos[1] -= 1
            elif action == 3:  # right
                new_pos[1] += 1

            # Check boundaries
            if (
                new_pos[0] < 0
                or new_pos[0] >= self.grid_size
                or new_pos[1] < 0
                or new_pos[1] >= self.grid_size
            ):
                reward -= 5

            # Check walls
            elif tuple(new_pos) in self.room_walls:
                reward -= 5

            else:
                self.robot_pos = new_pos
                reward -= 1

        # Deliver action
        elif action == 4:
            patient_index = self._get_patient_index(self.robot_pos)

            if patient_index is not None and self.delivered[patient_index] == 0:
                self.delivered[patient_index] = 1
                reward += 15
            else:
                reward -= 2

        # Exit logic
        if self.robot_pos == self.exit_pos:
            if self._all_medicines_delivered():
                reward += 30
                done = True
            else:
                reward -= 10

        self.steps += 1
        self.total_reward += reward

        # Safety cap
        if self.steps >= 100:
            done = True

        info = {
            "old_position": old_pos,
            "new_position": self.robot_pos.copy(),
            "delivered_status": self.delivered.copy(),
            "all_delivered": self._all_medicines_delivered(),
            "steps": self.steps,
            "total_reward": self.total_reward,
        }

        return self._get_obs(), reward, done, info

    def render(self):
        """Print hospital grid."""
        grid = np.full((self.grid_size, self.grid_size), ".", dtype=object)

        # Place walls
        for wall in self.room_walls:
            grid[wall] = "#"

        # Place patients
        for i, patient in enumerate(self.patient_positions):
            if self.delivered[i] == 0:
                grid[patient[0], patient[1]] = "P"
            else:
                grid[patient[0], patient[1]] = "D"

        # Place exit
        grid[self.exit_pos[0], self.exit_pos[1]] = "E"

        # Place robot
        grid[self.robot_pos[0], self.robot_pos[1]] = "R"

        print("\n".join(" ".join(row) for row in grid))
        print(f"Delivered: {self.delivered} | Steps: {self.steps} | Total Reward: {self.total_reward}")
        print("-" * 40)