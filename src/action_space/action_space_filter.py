from src.action_space.action import MAX_POSSIBLE_ACTIONS

class ActionSpaceFilter:

    def __init__(self):
        self.action_space = None
        self.action_on = [True] * MAX_POSSIBLE_ACTIONS

    def set_new_action_space(self, new_action_space):
        if self.is_identical_action_space_(new_action_space):
            print("DEBUG - Kept existing action space filter")
            return
        else:
            print("DEBUG - Warning ... DIFFERENT action space ... so filter reset!!!")
            self.action_space = new_action_space
            self.action_on = [True] * MAX_POSSIBLE_ACTIONS

    def should_show_action(self, index):
        return self.action_on[index]

    def set_filter_all(self):
        self.action_on = [True] * MAX_POSSIBLE_ACTIONS

    def set_filter_high_speed(self):
        self.action_on = [False] * MAX_POSSIBLE_ACTIONS

        for action in self.action_space:
            if action is not None and action.speed > 3:
                self.action_on[action.index] = True

    def set_filter_medium_speed(self):
        self.action_on = [False] * MAX_POSSIBLE_ACTIONS

        for action in self.action_space:
            if action is not None and 2 <= action.speed <= 3:
                self.action_on[action.index] = True

    def set_filter_low_speed(self):
        self.action_on = [False] * MAX_POSSIBLE_ACTIONS

        for action in self.action_space:
            if action is not None and action.speed < 2:
                self.action_on[action.index] = True

    def set_filter_straight(self):
        self.action_on = [False] * MAX_POSSIBLE_ACTIONS

        for action in self.action_space:
            if action is not None and abs(action.steering_angle) < 0.1:
                self.action_on[action.index] = True

    def is_identical_action_space_(self, new_action_space):
        if self.action_space is None:
            return False
        elif len(self.action_space) != len(new_action_space):
            return False
        else:
            for i in range(0, len(new_action_space)):
                a1 = self.action_space[i]
                a2 = new_action_space[i]

                if a1 is None and a2 is not None:
                    return False
                elif a1 is not None and a2 is None:
                    return False
                elif a1 is not None and not a1.is_same_as(a2):
                    return False

        return True




