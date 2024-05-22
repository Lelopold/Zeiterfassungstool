from task import Task


class Category:
    def __init__(self, name, cat_id):
        self.name = name
        self.tasks = []
        self.id = cat_id
        self.active = True
        self.active_task_count = 0
