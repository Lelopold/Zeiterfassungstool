class Task:
    def __init__(self, name: str, description: str, category: str, id_input: int):
        self.name = name
        self.description = description
        self.time_used = 0
        self.category = category
        self.id = id_input
        self.active = True
