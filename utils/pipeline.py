from utils.action import Action
import json

class Pipeline:

    def __init__(self, name, url, branch):
        self.name = name
        self.url = url
        self.branch = branch
        self.actions = []
        self.process = []  # Used on RUN commands, Process ID of all the processes running

    def add_action(self, new_action:Action):
        self.actions.append(new_action)

    def get_action(self, action_name):
        for action in self.actions:
            if action.name == action_name:
                return action
        return None

    def __str__(self):
        return self.name + " to " + self.url + " on " + self.branch

    def __dict__(self):
        new_obj = dict()
        new_obj['name'] = self.name
        new_obj['branch'] = self.branch
        new_obj['actions'] = []
        for x in self.actions:
            new_obj['actions'].append(str(x))
        return new_obj