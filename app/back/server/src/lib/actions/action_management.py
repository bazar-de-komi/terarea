"""_summary_
    File in charge of managing the actions
"""


class ActionManagement:
    def __init__(self, action):
        self.action = action

    def process(self, variables):
        self.action.process(variables)
