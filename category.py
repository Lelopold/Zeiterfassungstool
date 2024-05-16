from task import Task


class Category:
    def __init__(self, name):
        self.name = name
        self.active_tasks = []
        self.done_tasks = []
        self.time_used = 0
