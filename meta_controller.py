class HighLevelPolicy:
    """
    High-level HRL policy (meta-controller).

    Responsibilities:
    - Decide which sub-task the robot should perform next
    - Track task sequence based on hospital state

    Sub-goals:
    1. navigate_to_patient
    2. deliver_medicine
    3. exit_hospital
    """

    def __init__(self, patient_positions, exit_pos):
        self.patient_positions = patient_positions
        self.exit_pos = exit_pos
        self.current_subgoal = "navigate_to_patient"

    def get_next_undelivered_patient(self, delivered_status):
        """
        Return the next patient position that still needs medicine.
        """
        for i, delivered in enumerate(delivered_status):
            if delivered == 0:
                return self.patient_positions[i]
        return None

    def select_subgoal(self, robot_pos, delivered_status):
        """
        Select the current sub-goal based on robot position and delivery progress.
        """
        next_patient = self.get_next_undelivered_patient(delivered_status)

        # If patients still need medicine
        if next_patient is not None:
            if robot_pos == next_patient:
                self.current_subgoal = "deliver_medicine"
            else:
                self.current_subgoal = "navigate_to_patient"
        else:
            # All deliveries complete -> exit
            if robot_pos == self.exit_pos:
                self.current_subgoal = "mission_complete"
            else:
                self.current_subgoal = "exit_hospital"

        return self.current_subgoal