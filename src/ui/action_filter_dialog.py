#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from tkinter import BooleanVar, Checkbutton
from src.ui.dialog import Dialog
from src.action_space.action_space_filter import ActionSpaceFilter


class ActionSpaceFilterDialog(Dialog):
    def __init__(self, parent):
        self.action_space_filter: ActionSpaceFilter = parent.action_space_filter

        self.action_choices = []

        for action in self.action_space_filter._action_space.get_all_actions():
            if action is not None:
                self.action_choices.append(BooleanVar(value=self.action_space_filter._action_on[action.get_index()]))

        super().__init__(parent, "Action Space Filter")

    def body(self, master):
        col = 0
        row = 0
        for i, action in enumerate(self.action_space_filter._action_space.get_all_actions()):
            Checkbutton(
                master, text=action.get_readable_with_index(),
                variable=self.action_choices[i]).grid(column=col, row=row, pady=3, padx=3)
            row += 1
            if row == 8:
                row = 0
                col += 1

        return None    # Returns widget to have initial focus

    def apply(self):
        for i, action in enumerate(self.action_space_filter._action_space.get_all_actions()):
            self.action_space_filter._action_on[action.get_index()] = self.action_choices[i].get()

        self.parent.reapply_action_space_filter()

    def validate(self):
        return True
