from task import Task


class Category:
    def __init__(self, name, id):
        self.name = name
        self.tasks = []
        self.id = id
        self.time_used = 0
        self.active = True
        self.active_task_count = 0