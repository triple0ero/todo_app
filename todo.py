class TodoList:
    def __init__(self, filename='data/tasks.txt'):
        self.filename = filename
        self.tasks = self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                return [line.strip().split('|') for line in file]
        except FileNotFoundError:
            return []

    def save(self):
        with open(self.filename, 'w') as file:
            file.writelines(f"{title}|{description}\n" for title, description in self.tasks)

    def add(self, title, description):
        self.tasks.append((title, description))
        self.save()

    def remove(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save()

    def get_tasks(self):
        return self.tasks