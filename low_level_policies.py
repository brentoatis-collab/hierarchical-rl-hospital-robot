import random


class LowLevelPolicies:
    """
    Low-level HRL policies.

    Responsibilities:
    - Navigate toward a target position
    - Deliver medicine when at a patient location
    - Navigate toward the hospital exit
    """

    def __init__(self):
        pass

    def _valid_move(self, pos, grid_size, walls):
        """
        Check whether a move is valid within grid boundaries
        and not blocked by a wall.
        """
        row, col = pos

        if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
            return False

        if tuple(pos) in walls:
            return False

        return True

    def navigate_to_target(self, robot_pos, target_pos, grid_size, walls):
        """
        Improved navigation policy:
        - Prioritizes movement toward the target
        - Avoids walls and boundaries
        - Uses fallback random exploration to escape local traps

        Returns:
        0 = up
        1 = down
        2 = left
        3 = right
        """
        row, col = robot_pos
        target_row, target_col = target_pos

        preferred_moves = []

        # Prioritize vertical movement toward target
        if row < target_row:
            preferred_moves.append((1, [row + 1, col]))  # down
        if row > target_row:
            preferred_moves.append((0, [row - 1, col]))  # up

        # Prioritize horizontal movement toward target
        if col < target_col:
            preferred_moves.append((3, [row, col + 1]))  # right
        if col > target_col:
            preferred_moves.append((2, [row, col - 1]))  # left

        # Shuffle to reduce deterministic looping
        random.shuffle(preferred_moves)

        # Try preferred moves first
        for action, next_pos in preferred_moves:
            if self._valid_move(next_pos, grid_size, walls):
                return action

        # Fallback exploration if preferred moves are blocked
        fallback_moves = [
            (0, [row - 1, col]),  # up
            (1, [row + 1, col]),  # down
            (2, [row, col - 1]),  # left
            (3, [row, col + 1]),  # right
        ]

        random.shuffle(fallback_moves)

        for action, next_pos in fallback_moves:
            if self._valid_move(next_pos, grid_size, walls):
                return action

        # Default fallback if no valid moves exist
        return 0

    def deliver_medicine(self, robot_pos, patient_positions, delivered_status):
        """
        Return the deliver action if the robot is currently on a patient
        who has not yet received medicine.

        Returns:
        4 = deliver
        None = no valid delivery action
        """
        for i, patient_pos in enumerate(patient_positions):
            if robot_pos == patient_pos and delivered_status[i] == 0:
                return 4

        return None

    def exit_hospital(self, robot_pos, exit_pos, grid_size, walls):
        """
        Navigate toward the hospital exit using the same target-based policy.
        """
        return self.navigate_to_target(
            robot_pos=robot_pos,
            target_pos=exit_pos,
            grid_size=grid_size,
            walls=walls,
        )